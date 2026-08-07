import { z } from "zod";

// Base Configuration Schema Validation Placeholder
export const BaseConfigSchema = z.object({
  appName: z.string().default("LeadScan AI"),
  environment: z.enum(["development", "staging", "production"]).default("development"),
  debug: z.boolean().default(false),
});

export type BaseConfig = z.infer<typeof BaseConfigSchema>;
