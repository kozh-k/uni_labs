const { HashTable } = require('./lab6');

describe('HashTable', () => {
   let h;
 
   beforeEach(() => {
     h = new HashTable(20);
     h.set('Третьяк', 'Петр');
   });

   test('hash', () => {
     expect(h.hash('Вяткин')).toBe(18);
   });
   
   test('get', () => {
     expect(h.get('Третьяк')).toBe(`Искомый элемент: Третьяк Петр`);
   });
 
   test('delete', () => {
     expect(h.delete('Сидор')).toBe(false);
   });
 
   test('update', () => {
     expect(h.update('Вяткин', 'Саня')).toBe(false);
   });
 });