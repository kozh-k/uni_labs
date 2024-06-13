const { Logical } = require('./lab2');

describe('Logical', () => {
  let l;

  beforeEach(() => {
    l = new Logical('(a|b)~(!c)');
    l.doTable();
  });

  describe('doTable', () => {
    it('', () => {
      expect(l.doTable()).toEqual(true);
    });
  });

  describe('doSDNF', () => {
    it('', () => {
      const expectedSDNF = '(!a & !b & c) | (!a & b & !c) | (a & !b & !c) | (a & b & !c)';
      expect(l.doSDNF()).toEqual(expectedSDNF);
    });
  });

  describe('doSKNF', () => {
    it('should generate the SKNF correctly', () => {
      const expectedSKNF = '(a | b | c) & (a | !b | !c) & (!a | b | !c) & (!a | !b | !c)';
      expect(l.doSKNF()).toEqual(expectedSKNF);
    });
  });

  describe('doNumberFormSDNF', () => {
    it('should generate the number form of SDNF correctly', () => {
      const expectedNumberFormSDNF = '(1, 2, 4, 6) &';
      expect(l.doNumberFormSDNF()).toEqual(expectedNumberFormSDNF);
    });
  });

  describe('doNumberFormSKNF', () => {
    it('should generate the number form of SKNF correctly', () => {
      const expectedNumberFormSKNF = '(0, 3, 5, 7) |';
      expect(l.doNumberFormSKNF()).toEqual(expectedNumberFormSKNF);
    });
  });

  describe('doIndexForm', () => {
    it('should generate the index form correctly', () => {
      const expectedIndexForm = 106;
      expect(l.doIndexForm()).toEqual(expectedIndexForm);
    });
  });
});