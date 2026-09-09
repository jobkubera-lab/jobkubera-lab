import { McpServer } from '@modelcontextprotocol/server';
import { serveStdio } from '@modelcontextprotocol/server/stdio';
import * as z from 'zod/v4';

const registry = {
  'kubera-hello-mcp': {
    sideEffect: 'READ_ONLY',
    tools: ['hello', 'utc_time']
  },
  'kubera-evidence-mcp': {
    sideEffect: 'PREPARE_ONLY',
    tools: ['create_evidence_record', 'verify_evidence_hash']
  },
  'kubera-ons-mcp': {
    sideEffect: 'READ_ONLY',
    tools: ['build_dataset_version_path', 'fetch_ons_json']
  },
  'kubera-tender-mcp': {
    sideEffect: 'PREPARE_ONLY',
    tools: ['score_normalized_opportunity', 'verify_tender_requirements', 'draft_bid_pack']
  },
  'kubera-local-mcp': {
    sideEffect: 'READ_ONLY',
    tools: ['validate_official_service_url', 'create_local_service_evidence']
  },
  'kubera-collector-mcp': {
    sideEffect: 'READ_ONLY',
    tools: ['compare_supplied_listings', 'filter_budget']
  },
  'kubera-document-mcp': {
    sideEffect: 'READ_ONLY',
    tools: ['fingerprint_document', 'find_exact_terms', 'split_document_chunks']
  },
  'kubera-business-mcp': {
    sideEffect: 'PREPARE_ONLY',
    tools: ['prepare_booking_request', 'prepare_customer_reply']
  }
} as const;

type ServerName = keyof typeof registry;

function isServerName(value: string): value is ServerName {
  return Object.prototype.hasOwnProperty.call(registry, value);
}

serveStdio(() => {
  const server = new McpServer({ name: 'kubera-mcp-gateway-reference', version: '0.1.0' });

  server.registerTool(
    'list-approved-routes',
    {
      description: 'List the deny-by-default KUBERA MCP route registry.',
      inputSchema: z.object({})
    },
    async () => ({
      content: [{ type: 'text', text: JSON.stringify(registry, null, 2) }]
    })
  );

  server.registerTool(
    'authorize-route',
    {
      description: 'Check whether a logical server/tool pair is allow-listed. This does not proxy or execute the tool.',
      inputSchema: z.object({
        server: z.string().min(1).max(120),
        tool: z.string().min(1).max(120)
      })
    },
    async ({ server: serverName, tool }) => {
      if (!isServerName(serverName)) {
        return {
          content: [{ type: 'text', text: JSON.stringify({ allowed: false, reason: 'unknown_server' }) }]
        };
      }

      const route = registry[serverName];
      const allowed = (route.tools as readonly string[]).includes(tool);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            allowed,
            server: serverName,
            tool,
            sideEffect: route.sideEffect,
            reason: allowed ? 'allow_list_match' : 'unknown_tool'
          })
        }]
      };
    }
  );

  return server;
});
