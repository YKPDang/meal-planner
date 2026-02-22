import { describe, expect, it } from 'vitest'

import { formatLocalDate, parseIngredientLine, parseTags } from '../utils'

describe('parseIngredientLine', () => {
  it('parses a line with a unit and item', () => {
    expect(parseIngredientLine('200g pasta')).toEqual({ unit: '200g', item: 'pasta' })
  })

  it('parses a single value as item without unit', () => {
    expect(parseIngredientLine('tomato')).toEqual({ unit: '', item: 'tomato' })
  })
})

describe('parseTags', () => {
  it('returns cleaned tag values', () => {
    expect(parseTags(' pasta, quick-lunch , , dinner ')).toEqual(['pasta', 'quick-lunch', 'dinner'])
  })
})


describe('formatLocalDate', () => {
  it('formats using local calendar date components', () => {
    const localDate = new Date(2026, 0, 5, 0, 0, 0)
    expect(formatLocalDate(localDate)).toBe('2026-01-05')
  })
})
