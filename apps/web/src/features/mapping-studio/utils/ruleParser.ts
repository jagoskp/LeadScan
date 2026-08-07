import { DOMEntity } from "../types/studio";

export function evaluateCriteria(
  entity: DOMEntity,
  operator: string,
  compareValue: string
): boolean {
  const val = entity.value.toLowerCase();
  const target = compareValue.toLowerCase();

  switch (operator) {
    case "Contains":
      return val.includes(target);
    case "Starts With":
      return val.startsWith(target);
    case "Ends With":
      return val.endsWith(target);
    case "Regex":
      try {
        const regex = new RegExp(compareValue, "i");
        return regex.test(entity.value);
      } catch {
        return false;
      }
    default:
      return false;
  }
}
