const {howMuchKanjiIsPresent, isValidKanji, isKanjiPresent} = require('japanese-moji')
const fs = require('fs')

class KanjiVsWords {
    constructor(readIface, parser) {
        this._readIface = readIface
        this._parser = parser
        this._kanjiCount = {}

        //持: {"持つ": 53, "持ち越せる": 1 }
        this._wordsSeenForKanji = {}
    }

    async processUta() {
        for await(let line of this._readIface) {
            let [num, manyougana, kundoku, hiragana] = line.split(';')
            await this._processRawLine(kundoku)
        }
        fs.writeFileSync('kanji.json', JSON.stringify(this._kanjiCount))
        fs.writeFileSync('words.json', JSON.stringify(this._wordsSeenForKanji))

    }

    async _processRawLine(line) {
        let parsed = this._parser.parse(line)
        let stack = [parsed]
        while(stack && stack.length) {
            const node = stack.pop()
            if('children' in node) {
                node.children.reverse().forEach(c => stack.push(c))
            }
            else if(node.type !== 'WhiteSpaceNode') {
                await this._addKanjiAndWord(node.data.basic_form)
            }
        }
    }
    async _addKanjiAndWord(lemma) {
        if(howMuchKanjiIsPresent(lemma) > 0) {
            for(let i = 0; i < lemma.length; ++i) {
                if(isValidKanji(lemma[i])) {
                    this._addKanji(lemma[i])
                    this._addWordForKanji(lemma[i], lemma)
                }
              }

        }
    }

    _addKanji(lemma) {
        if(lemma in this._kanjiCount) {
            this._kanjiCount[lemma]++
        }
        else
            this._kanjiCount[lemma] = 1
    }
    _addWordForKanji(kanji, lemma) {
        if(this._wordsSeenForKanji[kanji] === undefined) {
            this._wordsSeenForKanji[kanji] = {}
            this._wordsSeenForKanji[kanji][lemma] = 1
        }
        else if(lemma in this._wordsSeenForKanji[kanji]) {
            this._wordsSeenForKanji[kanji][lemma]++
        }
        else {
            this._wordsSeenForKanji[kanji][lemma] = 1
        }
    }
}

module.exports = { KanjiVsWords }