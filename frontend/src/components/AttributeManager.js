/** Class containing functions to manipulate the attributes */
export default class AttributeManager {
	/** Checks to see if the given name is also in the given list.
	 * @param {string} attributeName The name of the attribute to search for.
	 * @param {Array.<{attributeName: string}>} list The list of attributes to search through.
	 * @returns Is the attribute in the list.
	*/
	static isAttributeNameIn = (attributeName, list) => {
		let index;
		for (index = 0; index < list.length; index++) {
			if (list[index].attributeName === attributeName) {
				return true;
			}
		}
		return false;
	};

	/** An insersion sort for attributes.
	 * @param {Array.<{attributeName: string}>} attributes The list of attributes to sort.
	*/
	static sortAttributes = (attributes) => {
		let size = attributes.length;
		let index;
		for (index = 1; index < size; index++) {
			let pos = index - 1;
			let currentItem = attributes[index];
			while (pos >= 0 && currentItem.attributeName < attributes[pos].attributeName) {
				let temp = attributes[pos];
				attributes[pos] = attributes[pos + 1];
				attributes[pos + 1] = temp;
				pos -= 1;
			}
		}
		return attributes;
	};
}