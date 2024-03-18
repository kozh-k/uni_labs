class Binary {
   constructor(x1, x2) {
      this.x1 = x1;
      this.x2 = x2;
      this.binaryX1 = this.toBinary(x1);
      this.binaryX2 = this.toBinary(x2);
      this.reverseBinaryX1 = this.reverseBinaryCode(x1);
      this.reverseBinaryX2 = this.reverseBinaryCode(x2);
      this.additionalBinaryX1 = this.additionalBinaryCode(x1);
      this.additionalBinaryX2 = this.additionalBinaryCode(x2);
   }

   toBinary(number) {
      const temp = number;
      let binary = '';
      number = Math.abs(number);
      if (number === 0) return '00000000';
      while (number > 0) {
          binary = (number % 2) + binary;
          number = Math.floor(number / 2);
      }
      while (binary.length < 8) {
          binary = '0' + binary;
      }
      return temp < 0 ? '1 ' + binary : '0 ' + binary;
   }

   fromBinary(binary) {
      const sign = binary[0] === '1' ? -1 : 1;
      const digits = binary.substring(2);
      const number = parseInt(digits, 2);
      return sign * number;
   }

   fromBinaryNoSign(x) {
      return parseInt(x, 2);
   }

   reverseBinaryCode(number) {
      const numberBin = this.toBinary(number);
      if (number >= 0) return numberBin;
      return numberBin.toString().split('').map((el, ind) => {
         if (ind > 1) {
            return el === '0' ? '1' : '0'
         } else return el;
      }).join('');
   }

   additionalBinaryCode(number) {
      if (number >= 0) return this.toBinary(number);
      number++;
      return this.reverseBinaryCode(number);
   }

   addAdditionalBinary(x1, x2) {
      let binX1 = this.reverseBinaryCode(x1).split(' ')[1];
      if (!binX1) binX1 = '00000000';
      let binX2 = this.reverseBinaryCode(x2).split(' ')[1];
      const arr = binX1.split('').reverse().map((el, i) => (el = parseInt(el) + parseInt(binX2[binX2.length - i - 1])));
      for (let i = 0; i < arr.length; i++) {
         if (arr[i] > 1) {
            arr[i] -= 2;
            if (i + 1 === arr.length) {
               i = -1;
               arr[0] += 1;
               continue;
            }
            arr[i + 1] += 1;
         }
      }
      return x1 + x2 < 0 ? "1 " + arr.reverse().map((el) => (el == "0" ? "1" : "0")).join('') : "0 " + arr.reverse().join("");
   }

   substractAdditionalBinary(x1, x2) {
      if (x1 === x2) return '0 00000000';
      return this.addAdditionalBinary(x1, -x2);
   }

   addBinaryArray(binaryArray) {
      if (!binaryArray || binaryArray.length === 0) return 'Array is empty';
      const maxLength = Math.max(...binaryArray.map(num => num.length));
      let result = '';
      let carry = 0;
      for (let i = 1; i <= maxLength; i++) {
         let sum = carry;
         for (const binaryNum of binaryArray) {
            const digit = binaryNum[binaryNum.length - i] ? parseInt(binaryNum[binaryNum.length - i]) : 0;
            sum += digit;
         }
         result = (sum % 2) + result;
         carry = Math.floor(sum / 2);
      }
      if (carry === 1) {
         result = '1' + result;
      }
      return result;
   }
   
   multiplyBinary(x1, x2) {
      let counter = 0;
      let result = [];
      for (let i = x2.length - 1; i >= 2; i--) {
          let sum = [];
          for (let j = x1.length - 1; j >= 2; j--) {
              sum.unshift(x1[j] * x2[i]);
          }
          for (let j = 0; j < counter; j++) {
              sum.push('0');
          }
          result.push(sum.join(''));
          counter++;
      }
      const res = this.addBinaryArray(result);
      return (parseInt(x1[0]) + parseInt(x2[0]) === 1 ? '1 ' : '0 ') + res;
   }
   
   removeSignAndLeadingZeros(binary) {
      if (binary === '0 00000000') return '0';
      return binary.slice(2).replace(/^0+/, '');
   }

   divideBinary(x1, x2) {
      let res = '';
      x1[0]+x2[0] == '10' || x1[0]+x2[0] == '01' ? res+='1 ' : res+='0 ';
      x1 = this.removeSignAndLeadingZeros(x1);
      x2 = this.removeSignAndLeadingZeros(x2);
      let substr = '';
      for (let i = 0; i < x1.length; i++) {
         substr += x1[i];
         if (this.fromBinaryNoSign(substr) >= this.fromBinaryNoSign(x2)) {
            break;
         }
      }
      let counter = substr.length;
      let diff, substrD, x2D;
      while (counter <= x1.length) {
         substrD = this.fromBinaryNoSign(substr);
         x2D = this.fromBinaryNoSign(x2);
         diff = this.removeSignAndLeadingZeros(this.substractAdditionalBinary(substrD, x2D));
         if(Math.abs(this.fromBinaryNoSign(diff)) === this.fromBinaryNoSign(x2)) ;
         if (this.fromBinaryNoSign(diff) >= 0 && this.fromBinaryNoSign(diff) < this.fromBinaryNoSign(x2)) {
            res+='1';
            substr = diff + x1[counter];
         } else {
            res+='0';
            substr+=x1[counter];
         }

         if (Math.abs(this.fromBinaryNoSign(diff)) === this.fromBinaryNoSign(x2) && counter === x1.length) {
            break;
         }

         if (counter === x1.length && this.fromBinaryNoSign(diff) !== 0) {
            diff = Math.abs(diff);
            res+=',';
            let counter2 = 0;
            substr = diff;
            while (this.fromBinaryNoSign(diff) !== 0 && counter2 < 5) {
               substr += '0';
               substrD = this.fromBinaryNoSign(substr);
               diff = this.removeSignAndLeadingZeros(this.substractAdditionalBinary(substrD, x2D));
               if (this.fromBinaryNoSign(diff) >= 0) {
                  res+='1';
               } else {
                  res+='0';
               }
               counter2++;
            }
         }
         counter++;
      }
      return res;
   }
}


class FloatBinary {
   constructor(x1, x2) {
      this.x1 = x1;
      this.x2 = x2;
      this.toBin(x1, x2);
      this.ieeeX1 = this.toBinaryFloat(this.x1, this.binaryX1);
      this.ieeeX2 = this.toBinaryFloat(this.x2, this.binaryX2);
   }

   toBinary(number) {
      const temp = number;
      let binary = '';
      number = Math.abs(number);
      if (number === 0) return '00000000';
      while (number > 0) {
          binary = (number % 2) + binary;
          number = Math.floor(number / 2);
      }
      while (binary.length < 8) {
          binary = '0' + binary;
      }
      return temp < 0 ? '1 ' + binary : '0 ' + binary;
   }

   fractionalToBin(number) {
      let binaryFraction = '';
      let fractionPart = Math.abs(number - Math.floor(number))
      let precision = 0;
      while (precision < 23) {
          fractionPart *= 2;
          const digit = Math.floor(fractionPart);
          binaryFraction += digit;
          fractionPart -= digit;
          precision++;
      }
   
      return binaryFraction;
   }

   toBin(x1, x2) {
      const first = new Binary(Number(x1.toString().split('.')[0]), Number(x1.toString().split('.')[1]));
      const second = new Binary(x2.toString().split('.')[0], x2.toString().split('.')[1]);
      this.binaryX1 = first.binaryX1 + '.' + this.fractionalToBin(this.x1);
      this.binaryX2 = second.binaryX1 + '.' + this.fractionalToBin(this.x2);
   }

   toBinaryFloat(number, bin) {
      let exp = 0;
      while (number >= 2) {
         number /= 2;
         exp++;
      }
      let mantissa = bin.match(/\d+$/g)[0].split('');
      for (let i=0; i<exp; i++) {
         mantissa.unshift(bin[9-i]);
         mantissa.pop();
      }
      const integer = this.toBinary(exp+127);
      return {
         value: integer + mantissa.join(''),
         point: integer + '.' + mantissa.join(''),
         mantissa: mantissa,
         exp: exp
      }
   }

   sumOfFloats(x1, x2) {
      const minExp = x1.exp < x2.exp ? JSON.parse(JSON.stringify(x1)) : JSON.parse(JSON.stringify(x2));
      const maxExp = x1.exp >= x2.exp ? JSON.parse(JSON.stringify(x1)) : JSON.parse(JSON.stringify(x2));

      if (minExp) {
         for (let i = 0; i < maxExp.exp - minExp.exp; i++) {
            minExp.mantissa.unshift(minExp.value[9-i]);
            minExp.mantissa.pop();
         }
      }
      minExp.mantissa = '1' + minExp.mantissa.join('');
      maxExp.mantissa = '1' + maxExp.mantissa.join('');
      console.log(minExp);
      console.log(maxExp);
      
      let bx1 = minExp.mantissa;
      let bx2 = maxExp.mantissa;
      let carry = 0;
      let result = '';

      for (let i = bx1.length - 1; i >= 0; i--) {
       const bit1 = parseInt(bx1[i]);
       const bit2 = parseInt(bx2[i]);
       const sum = bit1 + bit2 + carry;

       if (sum === 0) {
           result = '0' + result;
           carry = 0;
       } else if (sum === 1) {
           result = '1' + result;
           carry = 0;
       } else if (sum === 2) {
           result = '0' + result;
           carry = 1;
       } else if (sum === 3) {
           result = '1' + result;
           carry = 1;
       }
      }
      if (carry === 1) {
       result = '1' + result;
      }
      const n = result.length - 24;
      result = result.split('');
      if (n) {
         for (let i = 0; i < n; i++) {
            result.pop();
         }
      }
      result.shift();
      result = result.join('');
      return this.toBinary(maxExp.exp + n + 127) + result;
   }
}


const binary = new Binary(5, 4);
console.log(binary);

console.log('-------------------------------------');

console.log('сумма: ', binary.addAdditionalBinary(binary.x1, binary.x2), binary.fromBinary(binary.addAdditionalBinary(binary.x1, binary.x2)));
console.log('разность: ', binary.substractAdditionalBinary(binary.x1, binary.x2), binary.fromBinary(binary.substractAdditionalBinary(binary.x1, binary.x2)));
console.log('произведение: ', binary.multiplyBinary(binary.binaryX1, binary.binaryX2), binary.fromBinary(binary.multiplyBinary(binary.binaryX1, binary.binaryX2)));
console.log('деление: ', binary.divideBinary(binary.binaryX1, binary.binaryX2), binary.fromBinary(binary.divideBinary(binary.binaryX1, binary.binaryX2)));

console.log('-------------------------------------');


const float = new FloatBinary(10.5, 1.2);
console.log(float);

console.log('-------------------------------------');

console.log('сумма с пл. т.: ', float.sumOfFloats(float.ieeeX1, float.ieeeX2));

module.exports = { Binary, FloatBinary };