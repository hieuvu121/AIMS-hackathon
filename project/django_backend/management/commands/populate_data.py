from django.core.management.base import BaseCommand
from main.models import PageContent, CaseStudy, Method, AboutSection

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        # Create page content
        PageContent.objects.get_or_create(
            page='home',
            defaults={
                'title': 'Understanding of Modern Slavery',
                'subtitle': 'Our comprehensive approach to identifying and eliminating modern slavery in supply chains worldwide.',
                'content': {
                    'hero_title': 'BEYOND COMPLIANCE',
                    'hero_subtitle': 'A living data dashboard assessing modern slavery reporting across business sectors.',
                    'sections': [
                        {
                            'title': 'Data-Driven Insights',
                            'icon': '📊',
                            'description': 'We analyze modern slavery reporting across various business sectors to provide actionable insights and help organizations improve their compliance and ethical practices.'
                        },
                        {
                            'title': 'Comprehensive Assessment',
                            'icon': '🔍',
                            'description': 'Our methodology goes beyond basic compliance requirements to assess the depth and quality of modern slavery reporting across organizations.'
                        },
                        {
                            'title': 'Global Impact',
                            'icon': '🌍',
                            'description': 'Working with organizations worldwide to create more ethical and transparent global supply chains that protect vulnerable workers.'
                        }
                    ]
                }
            }
        )

        # Create case studies
        case_studies_data = [
            {
                'title': 'Technology Sector Analysis',
                'icon': '💻',
                'description': 'Our comprehensive analysis of modern slavery reporting in the technology sector reveals significant variations in transparency and accountability.',
                'details': 'We examine how major tech companies address forced labor in their supply chains, from raw material sourcing to manufacturing processes.',
                'order': 1
            },
            {
                'title': 'Fashion Industry Insights',
                'icon': '👗',
                'description': 'The fashion industry faces unique challenges in addressing modern slavery due to complex, multi-tier supply chains.',
                'details': 'We examine the role of certification programs, supplier partnerships, and technology solutions in improving supply chain transparency.',
                'order': 2
            },
            {
                'title': 'Agricultural Sector Challenges',
                'icon': '🌾',
                'description': 'Agricultural supply chains present particular challenges for modern slavery detection and prevention.',
                'details': 'Our research focuses on seasonal workers, migrant labor, and the informal economy\'s role in agricultural production.',
                'order': 3
            },
            {
                'title': 'Methodology and Data Sources',
                'icon': '📊',
                'description': 'Our case studies are based on publicly available information, including company reports and regulatory filings.',
                'details': 'We use a standardized framework to evaluate reporting quality, policy effectiveness, and implementation success.',
                'order': 4
            }
        ]

        for data in case_studies_data:
            CaseStudy.objects.get_or_create(
                title=data['title'],
                defaults=data
            )

        # Create methods
        methods_data = [
            {
                'title': 'Assessment Framework',
                'icon': '📋',
                'description': 'Our methodology is built on a robust framework that evaluates modern slavery reporting across multiple dimensions.',
                'details': 'We assess policy development, implementation effectiveness, transparency levels, and stakeholder engagement to provide a comprehensive view.',
                'order': 1
            },
            {
                'title': 'Data Collection Process',
                'icon': '📊',
                'description': 'We systematically collect data from multiple sources to ensure comprehensive coverage and accuracy.',
                'details': 'Our process includes automated data extraction, manual verification, and expert review to maintain high standards of data quality.',
                'order': 2
            },
            {
                'title': 'Evaluation Criteria',
                'icon': '⚖️',
                'description': 'Our evaluation criteria are based on international standards and best practices in modern slavery reporting.',
                'details': 'We assess policy comprehensiveness, implementation effectiveness, transparency levels, and stakeholder engagement.',
                'order': 3
            },
            {
                'title': 'Scoring Methodology',
                'icon': '📈',
                'description': 'Our scoring system uses a weighted approach that reflects the relative importance of different aspects.',
                'details': 'Scores are calculated based on policy quality, implementation effectiveness, and transparency levels.',
                'order': 4
            },
            {
                'title': 'Reporting and Analysis',
                'icon': '📝',
                'description': 'Our analysis includes trend identification, sector comparisons, and best practice documentation.',
                'details': 'We provide actionable insights and recommendations to help organizations improve their modern slavery reporting.',
                'order': 5
            },
            {
                'title': 'Stakeholder Engagement',
                'icon': '🤝',
                'description': 'We work closely with stakeholders to ensure our methodology remains relevant and effective.',
                'details': 'Regular feedback from organizations, NGOs, and experts helps us continuously improve our assessment approach.',
                'order': 6
            }
        ]

        for data in methods_data:
            Method.objects.get_or_create(
                title=data['title'],
                defaults=data
            )

        # Create about sections
        about_sections_data = [
            {
                'title': 'Our Mission',
                'icon': '🎯',
                'description': 'Light Carriers is dedicated to eliminating modern slavery from global supply chains through comprehensive data analysis, transparent reporting, and collaborative action.',
                'details': 'We believe that by shining a light on modern slavery reporting practices, we can drive meaningful change and protect vulnerable workers worldwide.',
                'order': 1
            },
            {
                'title': 'Our Approach',
                'icon': '🔬',
                'description': 'We use data-driven insights to assess modern slavery reporting across business sectors, identifying trends, gaps, and best practices.',
                'details': 'Our approach combines quantitative analysis with qualitative assessment, incorporating stakeholder feedback and expert opinions.',
                'order': 2
            },
            {
                'title': 'Our Team',
                'icon': '👥',
                'description': 'Our team brings together experts in human rights, supply chain management, data analysis, and policy development.',
                'details': 'We have extensive experience working with multinational corporations, NGOs, and government agencies to address modern slavery issues.',
                'order': 3
            },
            {
                'title': 'Our Impact',
                'icon': '🌟',
                'description': 'Since our founding, we have helped hundreds of organizations improve their modern slavery reporting and compliance efforts.',
                'details': 'Our data and insights have been used by businesses, investors, and policymakers to make informed decisions and drive positive change.',
                'order': 4
            },
            {
                'title': 'Our Values',
                'icon': '💎',
                'description': 'We are committed to transparency, accountability, and collaboration in all our work.',
                'details': 'We believe that addressing modern slavery requires a collective effort and that all stakeholders have a role to play.',
                'order': 5
            },
            {
                'title': 'Our Future',
                'icon': '🚀',
                'description': 'We are continuously evolving our methods and expanding our reach to create a more ethical global economy.',
                'details': 'Our vision is a world where all supply chains are transparent, accountable, and free from modern slavery.',
                'order': 6
            }
        ]

        for data in about_sections_data:
            AboutSection.objects.get_or_create(
                title=data['title'],
                defaults=data
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )

