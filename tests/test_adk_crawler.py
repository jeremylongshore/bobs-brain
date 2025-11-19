"""
Unit tests for ADK documentation crawler.

Tests configuration, crawling logic, extraction, chunking, and upload pipeline.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from tools.config import CrawlerConfig, load_config
from tools.adk_docs_crawler import ADKDocsCrawler
from tools.adk_docs_extract import ContentExtractor
from tools.adk_docs_chunker import DocumentChunker


class TestConfig:
    """Test configuration loading and validation."""

    def test_load_config_with_defaults(self, monkeypatch):
        """Test config loading with minimum required variables."""
        monkeypatch.setenv("GCP_PROJECT_ID", "test-project")

        config = load_config()

        assert config.project_id == "test-project"
        assert config.docs_bucket == "test-project-adk-docs"
        assert config.crawl_delay_seconds == 1.0
        assert config.max_chunk_tokens == 1500

    def test_load_config_with_custom_values(self, monkeypatch):
        """Test config loading with custom values."""
        monkeypatch.setenv("GCP_PROJECT_ID", "test-project")
        monkeypatch.setenv("BOB_DOCS_BUCKET", "custom-bucket")
        monkeypatch.setenv("CRAWL_DELAY_SECONDS", "2.5")
        monkeypatch.setenv("MAX_CHUNK_TOKENS", "2000")

        config = load_config()

        assert config.project_id == "test-project"
        assert config.docs_bucket == "custom-bucket"
        assert config.crawl_delay_seconds == 2.5
        assert config.max_chunk_tokens == 2000

    def test_load_config_missing_project_id(self, monkeypatch):
        """Test config loading fails without project ID."""
        monkeypatch.delenv("GCP_PROJECT_ID", raising=False)

        with pytest.raises(ValueError, match="GCP_PROJECT_ID"):
            load_config()

    def test_config_validation_negative_delay(self, monkeypatch):
        """Test config validation rejects negative delay."""
        monkeypatch.setenv("GCP_PROJECT_ID", "test-project")

        with pytest.raises(ValueError):
            CrawlerConfig(
                project_id="test-project",
                docs_bucket="test-bucket",
                crawler_sa_email=None,
                crawl_delay_seconds=-1.0,
                max_chunk_tokens=1500,
                start_url="https://example.com",
                tmp_dir="./tmp"
            )


class TestCrawler:
    """Test web crawler functionality."""

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return CrawlerConfig(
            project_id="test-project",
            docs_bucket="test-bucket",
            crawler_sa_email=None,
            crawl_delay_seconds=0.1,
            max_chunk_tokens=1500,
            start_url="https://google.github.io/adk-docs/",
            tmp_dir="./tmp"
        )

    @pytest.fixture
    def crawler(self, config):
        """Create test crawler instance."""
        return ADKDocsCrawler(config)

    def test_normalize_url(self, crawler):
        """Test URL normalization."""
        tests = [
            ("https://example.com/page", "https://example.com/page"),
            ("https://example.com/page/", "https://example.com/page"),
            ("https://example.com/page#anchor", "https://example.com/page"),
            ("https://example.com/page?query=1", "https://example.com/page"),
        ]

        for input_url, expected in tests:
            assert crawler.normalize_url(input_url) == expected

    def test_is_valid_url(self, crawler):
        """Test URL validation logic."""
        base = "https://google.github.io/adk-docs/"

        # Valid URLs
        assert crawler.is_valid_url("https://google.github.io/adk-docs/guide", base)
        assert crawler.is_valid_url("https://google.github.io/adk-docs/api/reference", base)

        # Invalid URLs
        assert not crawler.is_valid_url("https://other-domain.com/page", base)
        assert not crawler.is_valid_url("http://google.github.io/adk-docs/page", base)  # http not https
        assert not crawler.is_valid_url("https://google.github.io/other-docs/page", base)
        assert not crawler.is_valid_url("https://google.github.io/adk-docs/file.pdf", base)

    def test_extract_links(self, crawler):
        """Test link extraction from HTML."""
        html = """
        <html>
            <body>
                <a href="https://google.github.io/adk-docs/page1">Page 1</a>
                <a href="https://google.github.io/adk-docs/page2">Page 2</a>
                <a href="https://external.com/page">External</a>
                <a href="relative/path">Relative</a>
            </body>
        </html>
        """

        base_url = "https://google.github.io/adk-docs/"
        links = crawler.extract_links(html, base_url)

        assert "https://google.github.io/adk-docs/page1" in links
        assert "https://google.github.io/adk-docs/page2" in links
        assert "https://google.github.io/adk-docs/relative/path" in links
        assert "https://external.com/page" not in links  # External link filtered


class TestExtractor:
    """Test content extraction."""

    @pytest.fixture
    def extractor(self):
        """Create test extractor instance."""
        return ContentExtractor()

    def test_extract_code_blocks(self, extractor):
        """Test code block extraction."""
        html = """
        <html>
            <body>
                <pre><code class="language-python">def hello():
    print("world")</code></pre>
                <pre><code>plain text</code></pre>
            </body>
        </html>
        """

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        code_blocks = extractor.extract_code_blocks(soup)

        assert len(code_blocks) == 2
        assert code_blocks[0]['language'] == 'python'
        assert 'def hello()' in code_blocks[0]['code']
        assert code_blocks[1]['language'] == 'text'

    def test_extract_content(self, extractor):
        """Test full content extraction."""
        html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Main Heading</h1>
                <p>Introduction paragraph.</p>
                <h2>Subheading</h2>
                <p>Section content.</p>
                <pre><code class="language-python">code here</code></pre>
            </body>
        </html>
        """

        doc = extractor.extract_content(
            html=html,
            url="https://example.com/test",
            doc_id="test123",
            title="Test Page",
            timestamp="2025-11-19T00:00:00Z"
        )

        assert doc['doc_id'] == "test123"
        assert doc['url'] == "https://example.com/test"
        assert doc['title'] == "Test Page"
        assert len(doc['sections']) > 0
        assert doc['source_type'] == 'adk-docs'


class TestChunker:
    """Test document chunking."""

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return CrawlerConfig(
            project_id="test-project",
            docs_bucket="test-bucket",
            crawler_sa_email=None,
            crawl_delay_seconds=1.0,
            max_chunk_tokens=100,  # Small for testing
            start_url="https://example.com",
            tmp_dir="./tmp"
        )

    @pytest.fixture
    def chunker(self, config):
        """Create test chunker instance."""
        return DocumentChunker(config)

    def test_estimate_tokens(self, chunker):
        """Test token estimation."""
        text = "a" * 400  # 400 characters
        tokens = chunker.estimate_tokens(text)
        assert tokens == 100  # 400 / 4

    def test_chunk_small_document(self, chunker):
        """Test chunking a small document."""
        doc = {
            'doc_id': 'test123',
            'url': 'https://example.com/test',
            'title': 'Test Doc',
            'sections': [
                {
                    'heading_path': ['Main'],
                    'text': 'Short text.',
                    'code_blocks': []
                }
            ],
            'last_crawled_at': '2025-11-19T00:00:00Z',
            'source_type': 'adk-docs'
        }

        chunks = chunker.chunk_document(doc)

        assert len(chunks) == 1
        assert chunks[0]['doc_id'] == 'test123'
        assert chunks[0]['text'] == 'Short text.'

    def test_chunk_large_section(self, chunker):
        """Test splitting a large section."""
        long_text = "This is a sentence. " * 100  # Very long text

        section = {
            'heading_path': ['Main'],
            'text': long_text,
            'code_blocks': []
        }

        chunks = chunker.split_long_section(section, max_tokens=100)

        assert len(chunks) > 1  # Should be split
        for chunk in chunks:
            assert chunker.estimate_tokens(chunk['text']) <= 100


class TestPipeline:
    """Integration tests for full pipeline."""

    def test_config_to_chunker_integration(self, monkeypatch):
        """Test that config flows through to chunker."""
        monkeypatch.setenv("GCP_PROJECT_ID", "test-project")
        monkeypatch.setenv("MAX_CHUNK_TOKENS", "2000")

        config = load_config()
        chunker = DocumentChunker(config)

        assert chunker.config.max_chunk_tokens == 2000


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
