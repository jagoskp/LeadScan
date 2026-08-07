import { Button } from "@leadscan/ui";

export default function AdminHome() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-background p-24 text-foreground">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <p className="fixed left-0 top-0 flex w-full justify-center border-b border-border bg-gradient-to-b from-background pb-6 pt-8 backdrop-blur-2xl lg:static lg:w-auto lg:rounded-xl lg:border lg:p-4">
          Console:&nbsp;
          <code className="font-bold text-red-400">Admin/Ops</code>
        </p>
      </div>

      <div className="flex flex-1 flex-col items-center justify-center text-center">
        <h1 className="text-5xl font-extrabold tracking-tight sm:text-6xl bg-clip-text text-transparent bg-gradient-to-r from-red-400 to-amber-400 mb-6">
          LeadScan Admin
        </h1>
        <p className="max-w-[600px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed mb-8">
          Enterprise administration and telemetry workspace shell.
        </p>
        <div className="flex gap-4">
          <Button variant="secondary">Manage Services</Button>
          <Button variant="outline">System Logs</Button>
        </div>
      </div>
    </main>
  );
}
