// shared_types/index.ts
// Tipos TypeScript compartilhados entre frontend e backend
export interface Item {
  id: number;
  title: string;
  description?: string;
}