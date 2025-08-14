#!/usr/bin/env python3
"""
PDF Report Generator for Diagnostic Reports
Converts AI analysis into professional PDF documents
"""

import io
import base64
from datetime import datetime
from typing import Dict
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT


class DiagnosticPDFGenerator:
    """Generate professional PDF diagnostic reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceBefore=20,
            spaceAfter=12,
            borderColor=colors.HexColor('#3498db'),
            borderWidth=0,
            borderPadding=0
        ))
        
        # Cost style (green)
        self.styles.add(ParagraphStyle(
            name='CostStyle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#27ae60'),
            leftIndent=20
        ))
        
        # Warning style (orange)
        self.styles.add(ParagraphStyle(
            name='WarningStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#e67e22'),
            leftIndent=20
        ))
        
        # Danger style (red)
        self.styles.add(ParagraphStyle(
            name='DangerStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#e74c3c'),
            leftIndent=20,
            fontName='Helvetica-Bold'
        ))
    
    def generate_diagnostic_pdf(self, record: Dict, ai_response: Dict) -> bytes:
        """Generate complete diagnostic PDF report"""
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Add header
        elements.extend(self._create_header(record))
        
        # Add equipment information
        elements.extend(self._create_equipment_section(record))
        
        # Add problem description
        elements.extend(self._create_problem_section(record))
        
        # Add bottom line recommendation
        elements.extend(self._create_bottom_line_section(ai_response))
        
        # Add cost breakdown
        elements.extend(self._create_cost_section(ai_response))
        
        # Add red flags
        if ai_response.get('red_flags'):
            elements.extend(self._create_red_flags_section(ai_response))
        
        # Add solutions
        elements.extend(self._create_solutions_section(ai_response))
        
        # Add questions for shop
        elements.extend(self._create_questions_section(ai_response))
        
        # Add parts needed
        if ai_response.get('parts_needed'):
            elements.extend(self._create_parts_section(ai_response))
        
        # Page break before full analysis
        elements.append(PageBreak())
        
        # Add full analysis
        elements.extend(self._create_full_analysis_section(ai_response))
        
        # Add footer
        elements.extend(self._create_footer())
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _create_header(self, record: Dict):
        """Create PDF header"""
        elements = []
        
        # Title
        elements.append(Paragraph("DIAGNOSTIC REPORT", self.styles['CustomTitle']))
        
        # Report info table
        data = [
            ['Submission ID:', record.get('submission_id', '')],
            ['Date:', datetime.now().strftime('%B %d, %Y')],
            ['Time:', datetime.now().strftime('%I:%M %p')],
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.grey))
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_equipment_section(self, record: Dict):
        """Create equipment information section"""
        elements = []
        
        elements.append(Paragraph("EQUIPMENT INFORMATION", self.styles['SectionHeader']))
        
        data = [
            ['Type:', record.get('equipment_type', 'N/A')],
            ['Brand:', record.get('equipment_brand', 'N/A')],
            ['Model:', record.get('equipment_model', 'N/A')],
            ['Serial Number:', record.get('equipment_serial', 'N/A')],
            ['Year:', str(record.get('equipment_year', 'N/A'))],
            ['Operating Hours:', str(record.get('equipment_hours', 'N/A'))],
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ecf0f1')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_problem_section(self, record: Dict):
        """Create problem description section"""
        elements = []
        
        elements.append(Paragraph("PROBLEM DESCRIPTION", self.styles['SectionHeader']))
        
        # Problem description
        problem_text = record.get('problem_description', 'No description provided')
        elements.append(Paragraph(problem_text, self.styles['Normal']))
        elements.append(Spacer(1, 10))
        
        # Error codes if present
        if record.get('error_codes'):
            error_codes = ', '.join(record['error_codes'])
            elements.append(Paragraph(f"<b>Error Codes:</b> {error_codes}", self.styles['Normal']))
            elements.append(Spacer(1, 10))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_bottom_line_section(self, ai_response: Dict):
        """Create bottom line recommendation section"""
        elements = []
        
        elements.append(Paragraph("🎯 BOTTOM LINE RECOMMENDATION", self.styles['SectionHeader']))
        
        bottom_line = ai_response.get('bottom_line', 'Professional diagnosis recommended')
        
        # Create bordered box for bottom line
        data = [[bottom_line]]
        table = Table(data, colWidths=[6*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f5e9')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#4caf50')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_cost_section(self, ai_response: Dict):
        """Create cost breakdown section"""
        elements = []
        
        elements.append(Paragraph("💸 ESTIMATED COSTS", self.styles['SectionHeader']))
        
        costs = ai_response.get('estimated_cost', {})
        
        data = [
            ['Fair Price:', f"${costs.get('fair', 0):,.2f}"],
            ['Minimum:', f"${costs.get('min', 0):,.2f}"],
            ['Maximum:', f"${costs.get('max', 0):,.2f}"],
        ]
        
        labor = ai_response.get('labor_hours', {})
        if labor.get('book') or labor.get('actual'):
            data.append(['Book Hours:', f"{labor.get('book', 0)} hours"])
            data.append(['Actual Hours:', f"{labor.get('actual', 0)} hours"])
        
        table = Table(data, colWidths=[2*inch, 2*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),  # Fair price bold
            ('FONTSIZE', (1, 0), (1, 0), 14),  # Fair price larger
            ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#27ae60')),  # Green
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f5e9')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_red_flags_section(self, ai_response: Dict):
        """Create red flags section"""
        elements = []
        
        elements.append(Paragraph("🚩 RED FLAGS TO WATCH FOR", self.styles['SectionHeader']))
        
        for flag in ai_response.get('red_flags', []):
            elements.append(Paragraph(f"• {flag}", self.styles['DangerStyle']))
            elements.append(Spacer(1, 5))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_solutions_section(self, ai_response: Dict):
        """Create recommended solutions section"""
        elements = []
        
        elements.append(Paragraph("✅ RECOMMENDED SOLUTIONS", self.styles['SectionHeader']))
        
        for i, solution in enumerate(ai_response.get('solutions', []), 1):
            elements.append(Paragraph(f"{i}. {solution}", self.styles['Normal']))
            elements.append(Spacer(1, 8))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_questions_section(self, ai_response: Dict):
        """Create questions for shop section"""
        elements = []
        
        elements.append(Paragraph("❓ QUESTIONS TO ASK YOUR SHOP", self.styles['SectionHeader']))
        
        for question in ai_response.get('questions_for_shop', []):
            elements.append(Paragraph(f"□ {question}", self.styles['Normal']))
            elements.append(Spacer(1, 8))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_parts_section(self, ai_response: Dict):
        """Create parts needed section"""
        elements = []
        
        elements.append(Paragraph("📦 PARTS NEEDED", self.styles['SectionHeader']))
        
        parts_data = [['Part Name', 'Part Number', 'Est. Price']]
        
        for part in ai_response.get('parts_needed', []):
            parts_data.append([
                part.get('part', ''),
                part.get('number', ''),
                f"${part.get('price', 0):,.2f}"
            ])
        
        if len(parts_data) > 1:
            table = Table(parts_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ecf0f1')),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            elements.append(table)
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_full_analysis_section(self, ai_response: Dict):
        """Create full analysis section"""
        elements = []
        
        elements.append(Paragraph("📋 FULL TECHNICAL ANALYSIS", self.styles['SectionHeader']))
        
        analysis_text = ai_response.get('analysis', 'No detailed analysis available')
        
        # Split analysis into paragraphs for better formatting
        for paragraph in analysis_text.split('\n\n'):
            if paragraph.strip():
                # Check if it's a header (starts with emoji or number)
                if paragraph.strip()[0] in '🎯🔍✅❓💸🚩⚖️🔧📦💬🕵️📊🛠️' or paragraph.strip()[0].isdigit():
                    elements.append(Paragraph(paragraph, self.styles['Heading3']))
                else:
                    elements.append(Paragraph(paragraph, self.styles['BodyText']))
                elements.append(Spacer(1, 10))
        
        return elements
    
    def _create_footer(self):
        """Create PDF footer"""
        elements = []
        
        elements.append(Spacer(1, 30))
        elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.grey))
        elements.append(Spacer(1, 10))
        
        footer_text = """
        <para align=center>
        <font size=10>
        This report was generated by DiagnosticPro's AI system with 30+ years of master technician expertise.<br/>
        Always verify recommendations with a qualified technician.<br/>
        © 2025 DiagnosticPro | support@diagnosticpro.io
        </font>
        </para>
        """
        
        elements.append(Paragraph(footer_text, self.styles['Normal']))
        
        return elements


# Utility function for easy PDF generation
def generate_diagnostic_pdf(record: Dict, ai_response: Dict) -> bytes:
    """Generate diagnostic PDF report"""
    generator = DiagnosticPDFGenerator()
    return generator.generate_diagnostic_pdf(record, ai_response)