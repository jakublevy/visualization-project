const {JapaneseParser} = require('nlcst-parse-japanese')
const readline = require('readline')
const {KanjiVsWords} = require('./KanjiVsWords')
const fs = require('fs');

(async () => {
    await main()
})()

async function main() {
    const parser = new JapaneseParser()
    await parser.ready()
    const fStream = fs.createReadStream('../data/manyoushuu.csv')
    const rl = readline.createInterface({input: fStream, crlfDelay: Infinity})
    //const rI = readline.createInterface({input: process.stdin, output: process.stdout, terminal: false});
    const kvsw = new KanjiVsWords(rl, parser)
    await kvsw.processUta()

}