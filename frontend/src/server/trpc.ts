// tRPC router configuration for HandForge
export interface TRPCContext {
  userId?: string;
}

export type ProcedureResolver<TInput, TOutput> = (opts: {
  input: TInput;
  ctx: TRPCContext;
}) => Promise<TOutput> | TOutput;

export class TRPCRouter {
  private routes: Record<string, ProcedureResolver<any, any>> = {};

  register<TInput, TOutput>(path: string, resolver: ProcedureResolver<TInput, TOutput>) {
    this.routes[path] = resolver;
  }

  async execute(path: string, input: any, ctx: TRPCContext = {}) {
    const resolver = this.routes[path];
    if (!resolver) {
      throw new Error(`Procedure not found: ${path}`);
    }
    return await resolver({ input, ctx });
  }
}
