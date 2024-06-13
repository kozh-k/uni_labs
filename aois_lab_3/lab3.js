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
  let arr = f.split('&');
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
  console.log('Этап склеивания 1: ', res1);
  let res2 = glue(res1);
  // console.log(res2);
  // let res = glue(res2);
  // do {
  //   const it1 = glue(arr);
  //   const it2 = glue(it1);
  //   res = it1;
  // } while(it1.join('') != it2.join(''))
  let result = res2.reduce((acc, el) => {
    acc += `${el.join('')} & `;
    return acc;
  },'');

  return result.slice(0, -2);
}

function minTable(f, r) {
  f = f.split('|');
  f.map((el, i, arr) => {
    arr[i] = el.replace(/!([a-zA-Z])/g, (match, char) => char.toUpperCase());
  });

  r = r.split('&');
  r = r.map(el => el.trim());

  let table = [];

  let headerRow = [''];
  headerRow = headerRow.concat(f);
  table.push(headerRow);

  for (let i = 0; i < r.length; i++) {
    let row = [r[i]];
    for (let j = 0; j < f.length; j++) {
      let contains = true;
      let fChars = f[j].split('');
      let rChars = r[i].split('');
      for (let k = 0; k < rChars.length; k++) {
        if (!fChars.includes(rChars[k])) {
          contains = false;
          break;
        }
      }
      row.push(contains ? 1 : 0);
    }
    table.push(row);
  }
  console.table(table);
  return true;
}



function carno(f) {
  f = f.split('&');
  // f.map((el, i, arr) => {
  //   arr[i] = el.replace(/!([a-zA-Z])/g, (match, char) => char.toUpperCase());
  // });
  f.map((el, ind, arr) => {
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
  
  function convert(nestedList) {
    function convertElement(element) {
      return element === element.toUpperCase() ? 0 : 1;
    }
  
    return nestedList.map(sublist => sublist.map(convertElement));
  }

  let zero_array = [[0, 0, 0, 0], [0, 0, 0, 0]];
  let carno = convert(f);
  for (let i = 0; i < carno.length; i++) {
    for (let j = 0; j < carno[i].length; j++) {
      if (JSON.stringify(carno[i]) === JSON.stringify([0, 0, 0])) {
        zero_array[0][0] = 1;
      } else if (JSON.stringify(carno[i]) === JSON.stringify([0, 1, 0])) {
        zero_array[0][3] = 1;
      } else if (JSON.stringify(carno[i]) === JSON.stringify([0, 1, 1])) {
        zero_array[0][2] = 1;
      } else if (JSON.stringify(carno[i]) === JSON.stringify([0, 0, 1])) {
        zero_array[0][1] = 1;
      } else if (JSON.stringify(carno[i]) === JSON.stringify([1, 0, 0])) {
        zero_array[1][0] = 1;
      } else if (JSON.stringify(carno[i]) === JSON.stringify([1, 1, 0])) {
        zero_array[1][3] = 1;
      } else if (JSON.stringify(carno[i]) === JSON.stringify([1, 1, 1])) {
        zero_array[1][2] = 1;
      } else if (JSON.stringify(carno[i]) === JSON.stringify([1, 0, 1])) {
        zero_array[1][1] = 1;
      }
    }
  }
  console.table(zero_array);
  return true;
}


const res = min('(abc)&(a!bc)&(!abc)&(!a!b!c)')
console.log('Расчетный метод: ', res);
console.log(`\n`);
console.log('Расчетно-табличный метод: ');
minTable('(abc)&(a!bc)&(!abc)&(!a∨!b!c)', res);
console.log(res);
console.log(`\n`);
console.log('Таблица карно: ');
carno('(abc)&(a!bc)&(!abc)&(!a∨!b!c)');
console.log(res);

module.exports = { glue, min, minTable, carno };