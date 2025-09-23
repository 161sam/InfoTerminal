import { 
  Brain, 
  FileText, 
  Scale,
  Shield,
  Search
} from 'lucide-react';
import { DomainConfig, Domain, ExampleText } from '../panels/types';

export const DOMAINS: DomainConfig[] = [
  {
    id: 'general' as Domain,
    name: 'General',
    icon: Brain,
    color: 'blue',
    description: 'General-purpose NLP analysis'
  },
  {
    id: 'legal' as Domain,
    name: 'Legal',
    icon: Scale,
    color: 'purple',
    description: 'Legal document analysis and compliance'
  },
  {
    id: 'documents' as Domain,
    name: 'Documents',
    icon: FileText,
    color: 'green',
    description: 'Document processing and analysis'
  },
  {
    id: 'ethics' as Domain,
    name: 'Ethics',
    icon: Shield,
    color: 'indigo',
    description: 'Ethical analysis and compliance'
  },
  {
    id: 'forensics' as Domain,
    name: 'Forensics',
    icon: Search,
    color: 'red',
    description: 'Forensic analysis and investigation'
  }
];

export const EXAMPLE_TEXTS: Record<Domain, ExampleText[]> = {
  general: [
    {
      title: "Financial Report Sample",
      text: "ACME Corporation reported Q3 revenues of $2.4M, with CEO John Smith stating that the London office expansion contributed significantly to growth. The company's partnership with TechFlow Solutions has opened new markets in Europe."
    },
    {
      title: "News Article Sample", 
      text: "Berlin, Germany - The European Central Bank announced yesterday that inflation rates have stabilized at 2.1%. ECB President Christine Lagarde emphasized the importance of maintaining monetary policy stability across the eurozone."
    }
  ],
  legal: [
    {
      title: "Contract Clause",
      text: "The Party agrees to comply with all applicable laws and regulations, including but not limited to GDPR Article 6(1)(a) regarding data processing consent, and shall indemnify the Company against any violations thereof."
    },
    {
      title: "Regulatory Compliance",
      text: "§23 ArbSchG requires employers to implement adequate safety measures. Non-compliance may result in penalties under Section 25 of the Occupational Safety and Health Act."
    }
  ],
  documents: [
    {
      title: "Technical Documentation",
      text: "System requirements: Python 3.8+, PostgreSQL 12+, minimum 8GB RAM. Installation procedure documented in README.md. Configuration files located in /etc/config/. Backup procedures follow ISO 27001 standards."
    },
    {
      title: "Meeting Minutes",
      text: "Meeting held on March 15, 2024. Attendees: John Doe (Project Manager), Sarah Smith (Lead Developer), Mike Johnson (QA). Decisions: Deploy v2.1 by April 1st, increase testing coverage to 85%."
    }
  ],
  ethics: [
    {
      title: "Ethics Policy",
      text: "Our organization commits to transparent AI practices, ensuring algorithmic fairness and preventing bias in automated decision-making systems. Regular audits will assess compliance with ethical AI frameworks."
    },
    {
      title: "Compliance Assessment",
      text: "Data privacy impact assessment reveals potential risks in user profiling algorithms. Recommendations include implementing differential privacy and conducting quarterly bias audits."
    }
  ],
  forensics: [
    {
      title: "Investigation Report",
      text: "Subject: Maria Rodriguez, DOB: 1985-03-15, last known address: 123 Main Street, New York. Email: m.rodriguez@example.com. Associated with Global Imports LLC and frequent transactions to Swiss bank account CH93 0076 2011 6238 5295 7."
    },
    {
      title: "Digital Evidence",
      text: "File metadata analysis: Document created 2024-03-15 14:23:45 UTC, last modified 2024-03-16 09:15:22 UTC. IP address 192.168.1.105 accessed system at timestamp 1710511425. Hash verification: SHA-256 matches reference."
    }
  ]
};
