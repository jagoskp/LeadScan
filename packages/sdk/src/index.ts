// LeadScan SDK Client Placeholder
// This will contain the client interface for interacting with LeadScan API.

export class LeadScanClient {
  private readonly baseUrl: string;

  constructor(options: { baseUrl: string }) {
    this.baseUrl = options.baseUrl;
  }

  getBaseUrl(): string {
    return this.baseUrl;
  }
}
