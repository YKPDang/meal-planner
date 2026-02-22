import { describe, expect, it } from 'vitest'

import { parseIngredientLine, parseTags } from '../utils'

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
