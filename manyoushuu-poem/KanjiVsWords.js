const {howMuchKanjiIsPresent, isValidKanji, CharacterSet, createStrictValidator} = require('japanese-moji')
const fs = require('fs')

class KanjiVsWords {
    constructor(readIface, parser) {
        this._readIface = readIface
        this._parser = parser
        this._kanjiCount = {}
        this._currentUtaNumName = undefined
        this._currentUtaNum = 1
        this._wordsSeenForKanji = {}
        this._moraeForUta = {}
        this._kanaValidatorOptions = {
            characterSets : [
                CharacterSet.Katakana,
                CharacterSet.KatakanaPhoneticExtension,
                CharacterSet.HalfWidthKatakana,
                CharacterSet.Hiragana
            ]
        }
        this.isValidKana = createStrictValidator(this._kanaValidatorOptions)
    }

    async processUta() {
        for await(let line of this._readIface) {
            let [num, manyougana, kundoku, hiragana] = line.split(';')
            this._currentUtaNumName = num
            await this._processRawLine(kundoku)
            await this._processHiragana(hiragana)
            ++this._currentUtaNum
        }
        fs.writeFileSync('../data/poem-kanji.json', JSON.stringify(this._kanjiCount))
        fs.writeFileSync('../data/poem-words.json', JSON.stringify(this._wordsSeenForKanji))
        fs.writeFileSync('../data/poem-morae.json', JSON.stringify(this._moraeForUta))

    }

    async _processHiragana(hiragana) {
        let split = hiragana.split(' ')
        let c = []
        let skip = false

        for(let i = 0; i < split.length; ++i) {
            c.push(0)
            for(let j = 0; j < split[i].length; ++j) {
                if(skip) {
                    if(split[i][j] === ']')
                        skip = false
                    continue
                }
                if(split[i][j] === '[')
                    skip = true
                else if(split[i][j] === '*')
                    c[c.length - 1]++
                else if(this.isValidKana(split[i][j]))
                    c[c.length - 1]++
            }
            if(c[c.length - 1] === 0)
                c.splice(c.length - 1, 1)
        }
        if(c[c.length - 1] === 0)
            c.splice(c.length - 1, 1)

        this._moraeForUta[this._currentUtaNum] = {}
        this._moraeForUta[this._currentUtaNum]['name'] = this._currentUtaNumName
        this._moraeForUta[this._currentUtaNum]['poemCount'] = c.length
        this._moraeForUta[this._currentUtaNum]['morae'] = c
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
        if(this._kanjiCount[this._currentUtaNum] === undefined) {
            this._kanjiCount[this._currentUtaNum] = {}
            this._kanjiCount[this._currentUtaNum]['name'] = this._currentUtaNumName
        }

        if(lemma in this._kanjiCount[this._currentUtaNum])
            this._kanjiCount[this._currentUtaNum][lemma]++

        else
            this._kanjiCount[this._currentUtaNum][lemma] = 1

    }
    _addWordForKanji(kanji, lemma) {
        if(this._wordsSeenForKanji[this._currentUtaNum] === undefined)
            this._wordsSeenForKanji[this._currentUtaNum] = {}
        this._wordsSeenForKanji[this._currentUtaNum]['name'] = this._currentUtaNumName

        if(this._wordsSeenForKanji[this._currentUtaNum][kanji] === undefined) {
            this._wordsSeenForKanji[this._currentUtaNum][kanji] = {}
            this._wordsSeenForKanji[this._currentUtaNum][kanji][lemma] = 1
        }
        else if(lemma in this._wordsSeenForKanji[this._currentUtaNum][kanji]) {
            this._wordsSeenForKanji[this._currentUtaNum][kanji][lemma]++
        }
        else {
            this._wordsSeenForKanji[this._currentUtaNum][kanji][lemma] = 1
        }
    }
}

module.exports = { KanjiVsWords }