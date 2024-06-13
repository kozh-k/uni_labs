const { glue, min, minTable, carno } = require('./lab3')

describe('Min', () => {
   let l;

   beforeEach(() => {
      const res = min('(!abc)|(a!bc)|(abc)');
   });

   describe('min', () => {
     it('', () => {
       expect(min('(abc)&(a!bc)&(!abc)&(!a!b!c)')).toEqual('ac & bc & ABC ');
     });
   });

   describe('minTable', () => {
     it('', () => {
       expect(minTable('(!abc)|(a!bc)|(abc)', min('(!abc)|(a!bc)|(abc)'))).toEqual(true);
     });
   });

   describe('carno', () => {
     it('', () => {
       expect(carno('(!abc)|(a!bc)|(abc)')).toEqual(true);
     });
   });
 });