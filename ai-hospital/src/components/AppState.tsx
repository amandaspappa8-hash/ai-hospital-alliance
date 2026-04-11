export function Loading() {
  return <div style={{ padding: 20 }}>Loading...</div>;
}

export function ErrorState({ message }: { message: string }) {
  return <div style={{ padding: 20, color: "red" }}>Error: {message}</div>;
}
