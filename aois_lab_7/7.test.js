const { Matrix16 } = require('./lab7');

describe('Matrix16', () => {
  let matrix;

  beforeEach(() => {
    matrix = new Matrix16([
      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
      [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
      [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
      [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
      [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
      [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
      [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
      [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
      [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
      [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
      [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
      [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    ]);
  });

  test('should create a Matrix16 instance', () => {
    expect(matrix).toBeInstanceOf(Matrix16);
  });

  test('should throw an error for an invalid matrix', () => {
    expect(() => new Matrix16([[1, 2], [3, 4]])).toThrowError('Matrix must be 16x16');
  });

  test('should read a column correctly', () => {
    expect(matrix.readColumn(2)).toEqual([
      1, 1, 1, 1, 1, 0,
      0, 1, 0, 1, 0, 1,
      0, 1, 0, 1
    ]);
  });

  test('should read a diagonal correctly', () => {
    expect(matrix.readDiagonal(2)).toEqual([
      0, 0, 1, 0, 0, 0,
      0, 0, 0, 0, 0, 0,
      0, 0, 1, 1
    ]);
  });

  test('should find a column correctly', () => {
    expect(matrix.findColumn([0, 1, 1, 1, 1])).toEqual({
      arr: [
        0, 1, 1, 1, 1, 1,
        1, 0, 0, 1, 0, 1,
        0, 1, 0, 1
      ],
      r: 2
    });
  });

  test('should apply f0 correctly', () => {
    expect(matrix.f0(2)).toEqual(null);
  });

  test('should apply f5 correctly', () => {
    expect(matrix.f5(2, 14)).toEqual(null);
  });

  test('should apply f10 correctly', () => {
    expect(matrix.f10(2, 15)).toEqual(null);
  });

  test('should apply f15 correctly', () => {
    expect(matrix.f15(2)).toEqual(null);
  });

  test('should add binary numbers correctly', () => {
    expect(matrix.addBinary('1010', '1001')).toBe('0011');
  });

  test('should calculate the sum correctly', () => {
    expect(matrix.sum([1, 1, 0])).toBe('1101010101000100');
  });
});