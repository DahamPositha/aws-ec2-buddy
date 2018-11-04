/**
 * Created by Daham Pathiraja on 5/29/18.
 *
 * All json related functions could go in this module
 */
const loadedConfigs = {};

/**
 * All types of operations with files will be done by static methods of this util class
 */
export default class FileUtils {

    /**
     * Reads configurations from a json formatted file
     * @param {!string} name - Filename, with extension, of the configuration to be loaded
     * @returns {object} - Configuration object
     */
    static loadConfigs(name) {
        if (loadedConfigs[name]) {
            return loadedConfigs[name];
        }
        loadedConfigs[name] = require(`${process.cwd()}/localConfigs/` + name);
        return loadedConfigs[name];
    }
}
