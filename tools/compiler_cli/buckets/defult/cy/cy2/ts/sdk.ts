// sdk.ts

export interface OptionDef<T extends readonly string[]> {
  readonly kind: "option";
  readonly description: string;
  readonly choices: T;
}

export interface SelectionDef<T extends readonly string[]> {
  readonly kind: "selection";
  readonly description: string;
  readonly choices: T;
}

export interface NamespaceDef {
  readonly [key: string]: OptionDef<any> | SelectionDef<any>;
}

// Accept a single object instead of two positional args
export function Option<const T extends readonly string[]>(
  params: { description: string; choices: T }
): OptionDef<T> {
  return { kind: "option", ...params };
}

export function Selection<const T extends readonly string[]>(
  params: { description: string; choices: T }
): SelectionDef<T> {
  return { kind: "selection", ...params };
}