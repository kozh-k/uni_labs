const { ChildProcess } = require("child_process");

class HashTable {
  constructor(size) {
    this.size = size;
    this.table = new Array(size);
  }

  hash(key) {
    const alph = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я'];
    key = key.toUpperCase();
    const v = alph.indexOf(key[0])*33 + alph.indexOf(key[1]);
    return v % this.size;
  }

  set(key, value) {
    let index = this.hash(key);
    let initialIndex = index;

    while (this.table[index] && this.table[index][0] !== key) {
      index = (index + 1) % this.size;
      if (index === initialIndex) {
        throw new Error('Hash table is full');
      }
    }

    if (!this.table[index]) {
      this.table[index] = [];
    }
    this.table[index] = [key, value];
  }

  get(key) {
    let index = this.hash(key);
    let initialIndex = index;
    while (this.table[index]) {
      if (this.table[index][0] === key) {
        return `Искомый элемент: ${this.table[index][0] + ' ' + this.table[index][1]}`;
      }
      index = (index + 1) % this.size;
      if (index === initialIndex) {
        return undefined;
      }
    }

    return 'Элемент не найден!';
  }

  delete(key) {
    let index = this.hash(key);
    let initialIndex = index;

    while (this.table[index]) {
      if (this.table[index][0] === key) {
        this.table[index] = undefined;
        return true;
      }
      index = (index + 1) % this.size;
      if (index === initialIndex) {
        return false;
      }
    }

    return false;
  }

  update(key, newName) {
    let index = this.hash(key);
    let initialIndex = index;
  
    while (this.table[index]) {
      if (this.table[index][0] === key) {
        this.table[index][1] = newName;
        return true;
      }
      index = (index + 1) % this.size;
      if (index === initialIndex) {
        return false;
      }
    }
  
    return false;
  }

  printTable() {
    console.table(this.table.reduce((acc, bucket, index) => {
      if (bucket) {
        acc.push({ Hash: index, Value: `${bucket[0]} - ${bucket[1]}` });
      }
      return acc;
    }, []));
  }
}

const hashTable = new HashTable(20);

hashTable.set('Вяткин', 'Иван');
hashTable.set('Третьяк', 'Петр');
hashTable.set('Сидоров', 'Сергей');
hashTable.set('Сидук', 'Андрей');
hashTable.set('Сикно', 'Андрей');

console.log(hashTable.get('Вяткин'));
console.log(hashTable.get('Третьяк'));
console.log(hashTable.get('Сидоров'));
console.log(hashTable.get('Сидук'));
console.log(hashTable.get('Сикно'));

hashTable.delete('Сидоров');
console.log(hashTable.get('Сидоров'));

hashTable.set('Сидоров', 'Сергей');

hashTable.printTable();
console.log(`\n`);

hashTable.update('Вяткин', 'Саня')

console.log(`\n`);
hashTable.printTable();

module.exports = { HashTable };