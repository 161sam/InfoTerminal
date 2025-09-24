import { useState } from "react";

type Options = {
  ingestAleph?: boolean;
  annotate?: boolean;
  seedGraph?: boolean;
  seedSearch?: boolean;
  reset?: boolean;
};

type State = {
  loading: boolean;
  progress: number;
  result: any;
  error: any;
};

export function useDemoLoader() {
  const [state, setState] = useState<State>({
    loading: false,
    progress: 0,
    result: null,
    error: null,
  });

  async function loadDemo(opts: Options) {
    setState({ loading: true, progress: 0, result: null, error: null });
    try {
      const res = await fetch("/api/demo/load", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(opts),
      });
      const data = await res.json();
      setState({ loading: false, progress: 100, result: data, error: null });
    } catch (e) {
      setState({ loading: false, progress: 0, result: null, error: e });
    }
  }

  async function resetDemo() {
    await fetch("/api/demo/reset", { method: "POST" });
  }

  return { ...state, loadDemo, resetDemo };
}
