export function formatLocalDate(value: Date) {
  const date = new Date(value)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

export function getMonday(value: Date) {
  const day = new Date(value)
  const d = day.getDay() || 7
  if (d !== 1) {
    day.setHours(-24 * (d - 1))
  }
  day.setHours(0, 0, 0, 0)
  return day
}
