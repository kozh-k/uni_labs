class Matrix16 {
  constructor(matrix) {
    if (matrix.length !== 16 || matrix.every(row => row.length !== 16)) {
      throw new Error('Matrix must be 16x16');
    }
    this.matrix = matrix;
  }

  readColumn(index) {
    if (index < 0 || index >= 16) {
      throw new Error('Index must be between 0 and 15');
    }
    let result = [];
    let row = index;
    let col = index;
    
    while (row < 16) {
      result.push(this.matrix[row][col]);
      row++;
    }

    row = 0;
    while (row < index) {
      result.push(this.matrix[row][col]);
      row++;
    }

    return result;
  }

  readDiagonal(index) {
    if (index < 0 || index >= 16) {
      throw new Error('Index must be between 0 and 15');
    }
    let result = [];
    let row = index;
    let col = 0;
  
    while (row < 16) {
      result.push(this.matrix[row][col]);
      row++;
      col++;
    }
  
    row = 0;
    col = 16 - index;
    while (col < 16) {
      result.push(this.matrix[row][col]);
      row++;
      col++;
    }
  
    return result;
  }

  findColumn(arr) {
    const m = this.matrix;
    let result = [];
    for (let i=0; i<16; i++) {
      if(result.length === 16) return {'arr': result, 'r': i-1};
      for (let j=0; j<16; j++) {
        if (m[j][i] !== arr[j] && j < arr.length) {
          result = [];
          break;
        } else {
          result.push(m[j][i]);
        }
      }
    }
    return null;
  }

  f0(index) {
    for (let i=0; i<16; i++) {
      this.matrix[i][index] = 0;
    }
    return null;
  }

  f5(index, col) {
    for (let i=0; i<16; i++) {
      this.matrix[i][index] = this.matrix[i][col];
    }
    return null;
  }

  f10(index, col) {
    for (let i=0; i<16; i++) {
      this.matrix[i][index] = Number(!this.matrix[i][col]);
    }
    return null;
  }

  f15(index) {
    for (let i=0; i<16; i++) {
      this.matrix[i][index] = 1;
    }
    return null;
  }

  addBinary(a, b) {
    let num1 = parseInt(a, 2);
    let num2 = parseInt(b, 2);
    let sum = num1 + num2;
    let binarySum = sum.toString(2);
    return binarySum.slice(-4);
  }

  sum(arr) {
    let col = this.findColumn(arr).arr;
  
    let intervals = {
      V: [],
      A: [],
      B: [],
      S: []
    };
  
    for (let i = 0; i < col.length; i++) {
      let value = col[i];
      if (i >= 0 && i <= 2) {
        intervals.V.push(value);
      } else if (i >= 3 && i <= 6) {
        intervals.A.push(value);
      } else if (i >= 7 && i <= 10) {
        intervals.B.push(value);
      } else if (i >= 11 && i <= 15) {
        intervals.S.push(value);
      }
    }
    let a = intervals.A.join('');
    let b = intervals.B.join('');
    let s = this.addBinary(a, b);
    col = intervals.V.join('') + a + b + '0' + s;
    return col;
  }
}

const matrix = [
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
];

const m = new Matrix16(matrix);
console.log('Считывание столбца: ');
console.log(m.readColumn(2));
console.log('Считывание по диагонали: ');
console.log(m.readDiagonal(2));
console.log('Поиск по соответствию: ');
console.log(m.findColumn([0, 1, 1, 1, 1]));
console.log('Логические ф-ции: ');
console.table(m.matrix);
m.f0(0);
console.table(m.matrix);
console.log('----------------------------------------------');
m.f5(1, 15);
console.table(m.matrix);
console.log('----------------------------------------------');
m.f10(2, 15);
console.table(m.matrix);
console.log('----------------------------------------------');
m.f15(3);
console.table(m.matrix);
console.log('----------------------------------------------');
console.log('Результат сложения ', m.sum([1, 1, 0]));
console.table(m.matrix);

module.exports = { Matrix16 };