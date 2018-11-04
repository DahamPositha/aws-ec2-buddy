/**
 * Created by Daham Pathiraja on 5/29/18.
 */
import csvWriterLib from 'csv-writer';

/**
 * This class is capable of converting json object into csv file.
 */
export default class CsvWriter {
    /**
     * Init services and variables
     */
    constructor(file) {
        const createCsvWriter = csvWriterLib.createObjectCsvWriter;
        this.csvWriter = createCsvWriter({
            path: file,
            header: [
                {id: 'Timestamp', title: 'Timestamp'},
                {id: 'SpotPrice', title: 'SpotPrice'}
            ]
        });
    }

    /**
     * This method writes JSON object into csv file.
     * @param data
     * @returns {Promise}
     */
    writeJsonAsCsv(data) {
        let _this = this;

        return new Promise((resolve, reject)=> {
            _this.csvWriter.writeRecords(data)
                .then(() => {
                    console.log('Successfully written into csv file');
                    return resolve();
                })
                .catch(()=> {
                    console.log('Error while writing into csv file');
                    return reject();
                });
        });

    }
}
