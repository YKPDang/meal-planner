export function parseIngredientLine(line: string) {
  const trimmed = line.trim()
  if (!trimmed) {
    return null
  }

  const [unit, ...item] = trimmed.split(' ')
  return {
    unit: item.length ? unit : '',
    item: item.length ? item.join(' ') : unit
  }
}

export function parseTags(input: string) {
  return input
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean)
}
