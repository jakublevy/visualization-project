const fs = require('fs')

class KanjiLevelScraper {
    constructor(browser, page, kanji) {
        this._browser = browser
        this._page = page
        this._outputFile = '../data/kanji-info.json'
        this._kanji = kanji
        this._kanjiInfo = {}
    }

    async scrapeAll() {
        for(const kanji in this._kanji)
            await this.scrape(kanji)

        fs.appendFileSync(this._outputFile, JSON.stringify(this._kanjiInfo))
    }
    async scrape(kanji) {
        await this._page.goto(`https://jisho.org/search/${kanji}%23kanji`)

        const jlptElm = await this._page.$x('//div[@class="jlpt"]/strong')
        const freqElm = await this._page.$x('//div[@class="frequency"]/strong')
        const strokesElm = await this._page.$x('//div[@class="kanji-details__stroke_count"]/strong')

        let jlpt, freq, strokes

        if(jlptElm.length === 1) {
            jlpt = parseInt((await jlptElm[0].evaluate(e => e.textContent)).slice(1))
        }
        else if(jlptElm > 1) {
            throw "Invalid number of JLPT elements matched"
        }
        else {
            jlpt = -1
        }
        if(freqElm.length === 1) {
            freq = parseInt(await freqElm[0].evaluate(e => e.textContent))
        }
        else if(freqElm > 1) {
            throw "Invalid number of freq elements matched"
        }
        else {
            freq = -1
        }
        if(strokesElm.length === 1) {
            strokes = parseInt(await strokesElm[0].evaluate(e => e.textContent))
        }
        else if(strokesElm > 1) {
            throw 'Invalid number of stroke elements matched'
        }
        this._kanjiInfo[kanji] = {jlpt: jlpt, freq: freq, strokes: strokes}
    }
}

module.exports = { KanjiLevelScraper }