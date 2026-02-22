export function parseIngredientLine(line) {
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

export function parseTags(input) {
  return input
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean)
}

export function formatLocalDate(value) {
  const date = new Date(value)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}
