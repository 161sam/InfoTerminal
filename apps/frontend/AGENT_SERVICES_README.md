# InfoTerminal Agent Services

## Overview

The InfoTerminal Agent Services provide AI-powered investigation and analysis capabilities through a unified interface. This system replaces the legacy nlp-service with a modern, extensible architecture supporting multiple AI agents and specialized investigation workflows.

## Architecture

### Core Components

1. **Enhanced Agent Page** (`/agent`)
   - Primary user interface for AI agent interactions
   - Multi-agent support with specialized capabilities
   - Real-time status monitoring and health checks
   - Enhanced message display with execution steps and references

2. **Agent Management Dashboard** (`/agents`)
   - Administrative interface for agent services
   - Service health monitoring and status dashboard
   - Capability management and configuration
   - Multi-tab interface for different management aspects

3. **Modular Agent Chat Component** (`/components/agents/AgentChat.tsx`)
   - Reusable chat interface for agent interactions
   - Configurable capabilities and tool restrictions
   - Support for multiple agent types and workflows

4. **Centralized Configuration** (`/lib/agent-config.ts`)
   - Unified configuration for all agent capabilities
   - Health check utilities and endpoint management
   - Feature flag support and environment configuration

## Agent Capabilities

### Available Agents

1. **Research Assistant** - Comprehensive research and fact-checking
2. **Graph Analyst** - Network analysis and relationship mapping
3. **Security Analyst** - Cybersecurity threat assessment and risk analysis
4. **Geospatial Analyst** - Location intelligence and spatial analysis
5. **Person Investigator** - Deep person profiling and background checks
6. **Financial Analyst** - Financial pattern analysis and compliance
7. **Document Analyst** - Advanced document processing and forensics
8. **Media Analyst** - Image/video analysis and media verification
9. **Web Investigator** - Deep web research and digital footprints
10. **AI Synthesizer** - Multi-source intelligence synthesis

### Capability Categories

- **Analysis**: Data analysis, document processing, statistical analysis
- **Investigation**: Person research, background checks, forensic analysis
- **Security**: Threat assessment, vulnerability analysis, compliance
- **Intelligence**: Information synthesis, pattern recognition, strategic analysis

## API Endpoints

### Core API Routes

- `GET /api/agent` - API overview and service information
- `POST /api/agent/chat` - Chat with AI agents
- `GET /api/agent/health` - Service health status
- `GET /api/agent/capabilities` - List available capabilities
- `POST /api/agent/capabilities` - Execute specific capability
- `POST /api/agent/playbooks` - Legacy playbook execution (backward compatibility)

### Service Configuration

```typescript
// Environment variables for agent configuration
NEXT_PUBLIC_AGENT_API=http://localhost:8610           // Primary agent service
NEXT_PUBLIC_DOCENTITIES_API=http://localhost:8613     // Document entities service
NEXT_PUBLIC_FLOWISE_API=http://localhost:8620         // Flowise integration
NEXT_PUBLIC_N8N_URL=http://localhost:5678             // n8n workflows

// Feature flags
NEXT_PUBLIC_FEATURE_AGENT=1                           // Enable agent services
NEXT_PUBLIC_FEATURE_MULTI_AGENT=1                     // Enable multi-agent support
NEXT_PUBLIC_FEATURE_WORKFLOWS=1                       // Enable workflow automation

// Agent behavior configuration
NEXT_PUBLIC_AGENT_DEFAULT_TYPE=research_assistant     // Default agent type
NEXT_PUBLIC_AGENT_MAX_ITERATIONS=10                   // Max execution steps
NEXT_PUBLIC_AGENT_INCLUDE_STEPS=true                  // Include execution steps
NEXT_PUBLIC_AGENT_TIMEOUT=300000                      // Request timeout (ms)
```

## Service Integration

### Backend Services

The agent system integrates with several backend services:

1. **agent-connector** (Port 8610) - Primary orchestration service
2. **doc-entities** (Port 8613) - Document processing and NLP
3. **flowise-connector** (Port 8620) - Advanced workflow processing

### Health Monitoring

All services include comprehensive health monitoring:

```typescript
// Check individual service health
const health = await checkAgentHealth(endpoint);

// Check all services
const allHealth = await checkAllAgentHealth();
```

## Migration from Legacy System

### Changes from nlp-service

The system has been migrated from the legacy nlp-service to the new doc-entities service:

- **Removed**: `NEXT_PUBLIC_NLP_API` configuration
- **Added**: `NEXT_PUBLIC_DOCENTITIES_API` configuration
- **Enhanced**: Multi-agent support and specialized capabilities
- **Improved**: Error handling, health monitoring, and status reporting

### Backward Compatibility

Legacy playbook functionality is maintained through the `/api/agent/playbooks` endpoint, which maps old playbook names to new capabilities:

- `InvestigatePerson` → `person_investigator`
- `FinancialRiskAssistant` → `financial_analyst`
- And other existing playbooks...

## Usage Examples

### Basic Agent Chat

```typescript
import { EnhancedAgentChat } from '@/components/agents/AgentChat';

// Use in any component
<EnhancedAgentChat 
  apiBaseUrl="/api/agent"
  enableWorkflows={true}
  maxHeight="600px"
/>
```

### Service Health Check

```typescript
import { checkAllAgentHealth } from '@/lib/agent-config';

const checkServices = async () => {
  const health = await checkAllAgentHealth();
  console.log('Service status:', health);
};
```

### Capability Execution

```typescript
// Execute a specific capability
const response = await fetch('/api/agent/capabilities', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    capability: 'research_assistant',
    context: 'Research topic: Climate change impacts',
    tools: ['web_search', 'fact_checking']
  })
});
```

## Development

### Adding New Capabilities

1. Define the capability in `agent-config.ts`:
```typescript
{
  id: 'new_agent',
  name: 'new_agent',
  displayName: 'New Agent',
  description: 'Description of the new agent',
  icon: YourIcon,
  color: 'blue',
  tools: ['tool1', 'tool2'],
  category: 'analysis',
  expertise: ['domain1', 'domain2']
}
```

2. Add the agent to the backend service
3. Test via the management dashboard

### Environment Setup

1. Ensure all backend services are running
2. Configure environment variables
3. Enable feature flags as needed
4. Access the management dashboard at `/agents`

## Troubleshooting

### Common Issues

1. **Services offline**: Check that backend containers are running
2. **Configuration errors**: Verify environment variables
3. **Timeout issues**: Adjust `NEXT_PUBLIC_AGENT_TIMEOUT`
4. **Feature not available**: Check feature flags

### Health Monitoring

Use the Agent Management Dashboard (`/agents`) to monitor service health and diagnose issues. The dashboard provides:

- Real-time service status
- Response time monitoring
- Error tracking and reporting
- Configuration verification

## Security Considerations

- All agent communications are logged for audit purposes
- Tool restrictions can be configured per capability
- Session management with unique identifiers
- Request timeout enforcement to prevent resource abuse

---

For more detailed information, see the individual component documentation and the InfoTerminal development guide.
