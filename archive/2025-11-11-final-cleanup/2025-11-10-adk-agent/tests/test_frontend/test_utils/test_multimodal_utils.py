# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest.mock import MagicMock, patch

import pytest

from frontend.utils.multimodal_utils import (
    format_content,
    get_gcs_blob_mime_type,
    gs_uri_to_https_url,
)


def test_format_content_text_only() -> None:
    """Test formatting plain text content"""
    content = "Hello world"
    formatted = format_content(content)
    assert formatted == "Hello world"


def test_format_content_single_image() -> None:
    """Test formatting content with a single image"""
    content = [{"type": "image_url", "image_url": {"url": "test.jpg"}}]
    formatted = format_content(content)
    assert '<img src="test.jpg"' in formatted
    assert 'width="100"' in formatted


def test_format_content_mixed() -> None:
    """Test formatting content with text and images"""
    content = [
        {"type": "text", "text": "Here's an image:"},
        {"type": "image_url", "image_url": {"url": "test.jpg"}},
    ]
    formatted = format_content(content)
    assert "Here's an image:" in formatted
    assert '<img src="test.jpg"' in formatted


@patch("google.cloud.storage.Client")
def test_get_gcs_blob_mime_type(mock_storage_client: MagicMock) -> None:
    """Test getting MIME type from GCS blob"""
    mock_blob = MagicMock()
    mock_blob.content_type = "image/jpeg"
    mock_bucket = MagicMock()
    mock_bucket.blob.return_value = mock_blob
    mock_storage_client.return_value.bucket.return_value = mock_bucket

    mime_type = get_gcs_blob_mime_type("gs://bucket/test.jpg")
    assert mime_type == "image/jpeg"


def test_gs_uri_to_https_url() -> None:
    """Test converting GCS URI to HTTPS URL"""
    gs_uri = "gs://bucket/folder/file.jpg"
    https_url = gs_uri_to_https_url(gs_uri)
    assert https_url == "https://storage.mtls.cloud.google.com/bucket/folder/file.jpg"


def test_gs_uri_to_https_url_invalid() -> None:
    """Test converting invalid GCS URI"""
    with pytest.raises(ValueError):
        gs_uri_to_https_url("invalid_uri")
