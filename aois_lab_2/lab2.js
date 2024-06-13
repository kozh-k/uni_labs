class Logical {
   constructor(exp) {
      this.exp = exp;
      this.matrix = null;
   }

   and = (a, b) => Number(a) && Number(b) ? '1' : '0';

   or = (a, b) => !Number(a) && !Number(b) ? '0' : '1';

   not = (a) => Number(a) ? '0' : '1';

   equals = (a, b) => Number(Number(a) === Number(b)).toString();

   impl = (a, b) => Number(a <= b).toString();

   check = (elem) => {
      switch (elem) {
         case '&':
            return this.and;
         case '|':
            return this.or;
         case '~':
            return this.equals;
         case '>':
            return this.impl;
      }
   }

   doTable() {
      console.log('expression:', this.exp, '\n');
      console.log('table of truth:');
      const variables = Array.from(new Set(this.exp.match(/[a-z]/g)));
      const numVariables = variables ? [...new Set(variables)].length : 0;

      const header = variables ? variables.join('\t') : '';
      console.log(header + '\tF');
      
      const table = [];
      for (let i = 0; i < Math.pow(2, numVariables); i++) {
         const row = [];
         for (let j = numVariables - 1; j >= 0; j--) {
            row.push((i >> j) & 1);
         }
         table.push(row);
      }

      let matrix = [];

      table.forEach(row => {
         let result = this.exp;
         variables.forEach((variable, index) => {
            result = result.replace(new RegExp(variable, 'g'), row[index]);
         });
         
         while(result.length > 1) {
            for (let i = 0; i < result.length; i++) {
               if (result[i] === '!' && (result[i + 1] === '0' || result[i + 1] === '1')) {
                  const num = this.not(result[i + 1]);
                  result = result.slice(0, i-1) + num + result.slice(i + 3);
               } else if ((result[i] === '0' || result[i] === '1') && (/[&|~>]/.test(result[i + 1])) && (result[i + 2] === '0' || result[i + 2] === '1')) {
                  const num = this.check(result[i + 1])(result[i], result[i + 2]);
                  result = result.slice(0, i-1) + num + result.slice(i + 4);
               }
   
   
            }

            if(!/\(|\)/.test(result)) {
               for(let i=0; i < result.length; i++) {
                  if (result[i] === '!' && (result[i + 1] === '0' || result[i + 1] === '1')) {
                     const num = this.not(result[i + 1]);
                     result = result.slice(0, i) + num + result.slice(i + 2);
                  } else if ((result[i] === '0' || result[i] === '1') && (/[&|~>]/.test(result[i + 1])) && (result[i + 2] === '0' || result[i + 2] === '1')) {
                     const num = this.check(result[i + 1])(result[i], result[i + 2]);
                     result = result.slice(0, i) + num + result.slice(i + 3);
                  }
               }
            }

         }
         console.log(row.join('\t') + '\t' + result);

         row.push(Number(result));
         matrix.push(row);
      });
      this.matrix = matrix;
      //console.log(matrix);
      return true;
   }

   doSKNF() {
      console.log('SKNF:');
      const ones = structuredClone(this.matrix.filter(el => el[3] === 0));
      const vars = 'abcde';
      let result = '';
      ones.forEach((el, ind) => {
         result += ' & (';
         el.pop();
         el.forEach((e, i, arr) => {
            if (i === arr.length-1) {
               result += e == 1 ? `!${vars[i]}` : `${vars[i]}`;
            } else {
               result += e == 1 ? `!${vars[i]} | ` : `${vars[i]} | `;
            }
         })
         result += ')';
      })
      result = result.slice(3);
      console.log(result);
      return result;
   }

   doSDNF() {
      console.log('SDNF:');
      console.log(this.matrix);
      const m = this.matrix;
      const ones = structuredClone(m.filter(el => el[3] === 1));
      const vars = 'abcde';
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
      console.log(result);
      return result;
   }

   doNumberFormSDNF() {
      console.log('number form SDNF:');
      let result = this.matrix.reduce((acc, el, ind) => {
         return el[3] === 1 ? acc + ind.toString() + ', ' : acc;
      }, '(')
      result = result.slice(0, result.length-2);
      result += ') &';
      console.log(result);
      return result;
   }

   doNumberFormSKNF() {
      console.log('number form SKNF:');
      let result = this.matrix.reduce((acc, el, ind) => {
         return el[3] === 0 ? acc + ind.toString() + ', ' : acc;
      }, '(')
      result = result.slice(0, result.length-2);
      result += ') |';
      console.log(result);
      return result;
   }

   doIndexForm() {
      console.log('index form:');
      let result = this.matrix.reduce((acc, el) => {
         return acc + el[3].toString();
      }, '')
      console.log(result);
      result = parseInt(result, 2);
      console.log(result);
      return result;
   }
}

const l = new Logical('(a|b)~(!c)');
l.doTable();
console.log('\n');
l.doSDNF();
l.doSKNF();
l.doNumberFormSDNF();
l.doNumberFormSKNF();
l.doIndexForm();

module.exports = { Logical };