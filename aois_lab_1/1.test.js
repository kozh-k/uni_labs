const { Binary, FloatBinary } = require('./lab_1');

describe('Binary', () => {
  let binary;

  beforeEach(() => {
    binary = new Binary(5, 4);
  });

  test('addAdditionalBinary', () => {
    expect(binary.addAdditionalBinary(5, 4)).toBe('0 00001001');
  });

  test('substractAdditionalBinary', () => {
    expect(binary.substractAdditionalBinary(5, 4)).toBe('0 00000001');
  });

  test('multiplyBinary', () => {
    expect(binary.multiplyBinary('0 00000101', '0 00000100')).toBe('0 000000000010100');
  });

  test('divideBinary', () => {
    expect(binary.divideBinary('0 00000101', '0 00000100')).toBe('0 1,11');
  });
});


describe('FloatBinary', () => {
  let float;

  beforeEach(() => {
    float = new FloatBinary(10.5, 1.2);
  });

  test('fractionalToBin', () => {
    expect(float.fractionalToBin(10.5)).toBe('10000000000000000000000');
  });

  test('sumOfFloats', () => {
    const x1 = {
      value: '0 1000001001010000000000000000000',
      point: '0 10000010.01010000000000000000000',
      mantissa: [
        '0', '1', '0', '1', '0',
        '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0',
        '0', '0', '0'
      ],
      exp: 3
    };
    const x2 = {
      value: '0 0111111100110011001100110011001',
      point: '0 01111111.00110011001100110011001',
      mantissa: [
        '0', '0', '1', '1', '0',
        '0', '1', '1', '0', '0',
        '1', '1', '0', '0', '1',
        '1', '0', '0', '1', '1',
        '0', '0', '1'
      ],
      exp: 0
    };
    expect(float.sumOfFloats(x1, x2)).toBe('0 1000001110011011001100110011001');
  });
});