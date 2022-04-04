const assert = require('assert');
const fs = require('fs')

class Scraper {
    constructor(browser, page) {
        this._browser = browser
        this._page = page
        this._outputFile = '../data/manyoushuu.csv'
    }
    async scrapeAll() {
        for (let i = 1; i <= 20; ++i)
            await this.scrapeNth(i)
    }
    async scrapeNth(n) {
        await this.loadBook(n)

        const kundokuElms = await this._page.$x('//p[starts-with(text(), "[訓読]")]')
                                                                                                               // book 12
        const genbunElms = await this._page.$x('//p[starts-with(text(), "[原文]") or starts-with(text(), "[本文]")]')
        const kanaElms = await this._page.$x('//p[starts-with(text(), "[仮名]")]')
        const utaNumElms = await this._page.$x('(//font[@color="#800000"]/a)[position() > 1]')

        const kundoku = (await Promise.all(kundokuElms.map(e => e.evaluate(el => el.textContent)))).map(k => k.slice(4))
        const genbun = (await Promise.all(genbunElms.map(e => e.evaluate(el => el.textContent)))).map(g => g.slice(4))
        const kana = (await Promise.all(kanaElms.map(e => e.evaluate(el => el.textContent)))).map(k => k.slice(5)).map(k => k.replaceAll(',', ' '))
        const utaNum = await Promise.all(utaNumElms.map(e => e.evaluate(el => el.textContent)))

        if(n === 19) { // missing genbun 4170
            genbun.splice(31, 0, '白玉之 見我保之君乎 不見久尓 夷尓之乎礼婆 伊家流等毛奈之')
        }

        await this.appendToFile(utaNum, genbun, kundoku, kana)

    }
    async loadBook(n) {
        assert(n >= 1 && n <= 20, 'Invalid book number')
        if(n < 10)
            await this._page.goto(`https://jti.lib.virginia.edu/japanese/manyoshu/Man${n}Yos.html`)
        else
            await this._page.goto(`https://jti.lib.virginia.edu/japanese/manyoshu/Man${n}Yo.html`)
    }
    async appendToFile(utaNum, genbun, kundoku, kana) {
        assert((utaNum.length === genbun.length && genbun.length === kundoku.length && kundoku.length === kana.length), 'Scraping error')
        for(let i = 0; i < utaNum.length; ++i) {
            fs.appendFileSync(this._outputFile, `${utaNum[i]};${genbun[i]};${kundoku[i]};${kana[i]}\n`)
        }
    }
}

module.exports = { Scraper }