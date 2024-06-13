class bcd {
  constructor(n) {
    this.n = n;
    this.table = this.table();
  }

  sum(binaryNum) {
    if (binaryNum.length !== 4 || /[^01]/.test(binaryNum)) {
      throw new Error('Входное число должно быть 4-битным двоичным числом.');
    }
  
    let decimalNum = parseInt(binaryNum, 2);
    let resultDecimal = decimalNum + 2;
    let resultBinary = resultDecimal.toString(2).padStart(4, '0');
  
    return resultBinary;
  }

  shift(n) {
    if (n === '1000') return '0000';
    if (n === '1001') return '0001';
  }

  table() {
    let m = [
      ['0000', this.sum('0000')],
      ['0001', this.sum('0001')],
      ['0010', this.sum('0010')],
      ['0011', this.sum('0011')],
      ['0100', this.sum('0100')],
      ['0101', this.sum('0101')],
      ['0110', this.sum('0110')],
      ['0111', this.sum('0111')],
      ['1000', this.shift('1000')],
      ['1001', this.shift('1001')]
    ]
    this.table = m;
    return m;
  }
}


function glue(arr) {
  let res = [];

  let usedArr = new Array(arr.length).fill(false);
  
  for (let i=0; i<arr.length; i++) {
    for (let j=i+1; j<arr.length; j++) {
      let counter = 0;
      let r = '';
      
      if (arr[i].length === 2 && arr[j].length === 2) {
        if (arr[i][0] === arr[j][0] && arr[i][1].toUpperCase() === arr[j][1].toUpperCase()) {
          r += arr[i][0];
          res.push(r.split(''));
          usedArr[i] = true;
          usedArr[j] = true;
          continue;
        }
        if (arr[i][1] === arr[j][1] && arr[i][0].toUpperCase() === arr[j][0].toUpperCase()) {
          r += arr[i][1];
          res.push(r.split(''));
          usedArr[i] = true;
          usedArr[j] = true;
          continue;
        }
      }
      
      for (let n=0; n<arr[0].length; n++) {
        if (arr[i].length > 2 && arr[i][n] === arr[j][n]) {
          counter++;
          r += arr[i][n];
        }
      }
      
      if (counter >= arr[0].length-1) {
        res.push(r.split(''));
        usedArr[i] = true;
        usedArr[j] = true;
      }
    }
  }
  
  for (let i=0; i<arr.length; i++) {
    if (!usedArr[i]) {
      res.push(arr[i]);
    }
  }
  
  res = res.filter((value, index, self) =>
    index === self.findIndex((t) => (
      t.join('') === value.join('')
    ))
  );

  return res;
}


function min(f) {
  let arr = f.split('|');
  arr.map((el, ind, arr) => {
    el = el.split('');
    el.pop();
    el.shift();
    el.map((e, i, a) => {
      if (e === '!') {
        a[i+1] = a[i+1].toUpperCase();
        a.splice(i, 1);
      }
      return e;
    });
    arr[ind] = el;
    return el;
  })
  let res1 = glue(arr);
  //console.log('Этап склеивания 1: ', res1);
  let res2 = glue(res1);
  // console.log(res2);
  // let res = glue(res2);
  // do {
  //   const it1 = glue(arr);
  //   const it2 = glue(it1);
  //   res = it1;
  // } while(it1.join('') != it2.join(''))
  let result = res2.reduce((acc, el) => {
    acc += `${el.join('')} | `;
    return acc;
  },'');

  return result.slice(0, -2);
}


class sdnf {
  constructor(table1, table2) {
    this.table1 = table1;
    this.table2 = table2;
    this.sdnf1 =  null;
    this.sdnf2 =  null;
  }

  sdnf(t) {
    console.log('SDNF:');
      const m = t;
      const ones = structuredClone(m.filter(el => el[3] === 1));
      const vars = 'zvu';
      let result = '';
      ones.forEach((el, ind) => {
         result += ' | (';
         el.pop();
         el.forEach((e, i, arr) => {
            if (i === arr.length-1) {
               result += e == 0 ? `!${vars[i]}` : `${vars[i]}`;
            } else {
               result += e == 0 ? `!${vars[i]} & ` : `${vars[i]} & `;
            }
         })
         result += ')';
      })
      result = result.slice(3);
      result = result.replace(/\s|&/g, '');
      console.log(result);
      if (result === '(!z!vu)|(!zv!u)|(z!v!u)|(zvu)') {
        this.sdnf1 = result;
      } else {
        this.sdnf2 = result;
      }
      return result;
  }

  minSdnf1() {
    return min(this.sdnf1);
  }

  minSdnf2() {
    return min(this.sdnf2);
  }
}


let q = new bcd(2);
console.table(q.table);
console.log(`\n`);
let s = new sdnf([
  [ 0, 0, 0, 0 ],
  [ 0, 0, 1, 1 ],
  [ 0, 1, 0, 1 ],
  [ 0, 1, 1, 0 ],
  [ 1, 0, 0, 1 ],
  [ 1, 0, 1, 0 ],
  [ 1, 1, 0, 0 ],
  [ 1, 1, 1, 1 ]
], [
  [ 0, 0, 0, 0 ],
  [ 0, 0, 1, 0 ],
  [ 0, 1, 0, 1 ],
  [ 0, 1, 1, 0 ],
  [ 1, 0, 0, 1 ],
  [ 1, 0, 1, 0 ],
  [ 1, 1, 0, 1 ],
  [ 1, 1, 1, 1 ]
]);
s.sdnf(s.table1);
console.log(s.minSdnf1());
console.log(`\n`);
s.sdnf(s.table2);
console.log(s.minSdnf2());