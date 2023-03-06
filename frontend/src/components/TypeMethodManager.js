/** Class containing functions to manipulate the types and attributes */
export default class TypeMethodManager {
	/** Checks to see if the given attribute name is also in the given list.
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

	/** An insersion sort for attributes, references their names to compare.
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

	/** Checks to see if the given type name is also in the given list.
	 * @param {string} typeName The name of the type to search for.
	 * @param {Array.<{typeName: string}>} list The list of types to search through.
	 * @returns Is the type in the list.
	*/
	static isTypeNameIn = (typeName, list) => {
		let index;
		let length = list.length;
		for (index = 0; index < length; index++) {
			if (list[index].type_name === typeName) {
				return true;
			}
		}
		return false;
	};

	/** Binary search that returns the index of the target item.
	 * @param {[any]} list An ordered list of comparable items.
	 * @param {[any]} target The item to find.
	 * @returns {int} The index of the target or -1 if no match is found.
	 */
	static bin_search = (list, target) => {
		let start = 0;
		let end = list.length - 1;

		while (start <= end) {
			let mid = Math.floor((start + end) / 2);

			if (list[mid] < target) {
				start = mid + 1;
			}
			else if (list[mid] > target) {
				end = mid - 1;
			}
			else {
				return mid;
			}
		}
		return -1;
	};

	/** Search to find if all the items in the a list are in another list regardless of the lists' order.
	 * @param {[int]} bigList The list of all items.
	 * @param {[int]} smallList The list of items to check for.
	 * @returns Are all the items in the smallList are in the bigList.
	 */
	static doesContainAll = (bigList, smallList) => {
		bigList.sort();
		smallList.sort();
		let index = 0;
		let failed = false;
		while (index < smallList.length && !failed) {
			failed = this.bin_search(bigList, smallList[index]) < 0;
			index += 1;
		}
		return !failed;
	};

	/** Takes a list of attributes and extracts their ids.
	 * @param {[object]} list The list of attributes.
	 * @returns {[int]} The list of ids.
	 */
	static extractAttributeIds = (list) => {
		let newList = [];
		list.forEach(attribute => {
			newList.push(attribute.attributeID);
		});
		return newList;
	};

	/** Removes the given types from the given list of types
	 * @param {[object]} list The list of types
	 * @param {[int]} toRemove The list og type ids to remove
	 * @returns {[object]}The given list minus the items given to remove
	 */
	static removeTheseFromList(list, toRemove) {
		let newList = [];
		list.forEach(type => {
			if (!toRemove.includes(type.type_id)) {
				newList.push(type);
			}
		});
		return newList;
	}


	/** Finds the given index of the attribute where the attributeID matches.
	 * @param {[object]} list The list of attributes.
	 * @param {object} attribute The attribute to find.
	 * @returns {int} The index of the attribute in the list, -1 if not found.
	 */
	static getAttributeIndex = (list, attribute) => {
		let index;
		for (index = 0; index < list.length; index++) {
			if (list[index].attributeID === attribute.attributeID) {
				return index;
			}
		}
		return -1;
	};

	/** An insersion sort for attributes, refrences their ids to sort.
	 * @param {Array.<{attributeID: int}>} attributes The list of attributes to sort.
	 * @returns {[int]} The ids in ascending order.
	*/
	static get_sortedAttributes_byId = (attributes) => {
		let size = attributes.length;
		let index;
		for (index = 1; index < size; index++) {
			let pos = index - 1;
			let currentItem = attributes[index];
			while (pos >= 0 && currentItem.attributeID < attributes[pos].attributeID) {
				let temp = attributes[pos];
				attributes[pos] = attributes[pos + 1];
				attributes[pos + 1] = temp;
				pos -= 1;
			}
		}
		let ret = [];
		attributes.forEach(attribute => { ret.push(attribute.attributeID); });
		return ret;
	};

	/** Algorithm to find all the indexes of the current attributes in all that arn't in prev.
	 * @param {[object.<{attributeID: int}>]} curr The list of attributes to find.
	 * @param {[object.<{attributeID: int}>]} prev The list of the attributes to ignore.
	 * @param {[object.<{attributeID: int}>]} all The list of all possible attributes.
	 * @returns {[int]} The indexes of the attribute with reference to out.
	 */
	static getNewAttributeIndexes = (curr, prev, all) => {
		curr = this.get_sortedAttributes_byId(curr);
		prev = this.get_sortedAttributes_byId(prev);
		all = this.get_sortedAttributes_byId(all);
		let curr_p = 0;
		let all_i = 0;
		let out = [];
		while (curr_p < curr.length && all_i < all.length) {
			if (all[all_i] === curr[curr_p]) {
				if (this.bin_search(prev, curr[curr_p]) === -1) {
					out.push(all_i);
				}
				curr_p += 1;
			}
			all_i += 1;
		}
		return out;
	};

	/** Inserts an item into the given array.
	 * @param {*} item The item to insert.
	 * @param {int} index The index to insert at.
	 * @param {[*]} array The array to insert into.
	 * @returns {[*]} The newly inserted array.
	 * If the index is outof bounds of the array, no insertion is made.
	 */
	static insertInto = (item, index, array) => {
		if (index >= array.length) {
			console.warn('Index out of bounds of array. No new item inserted.');
			return array;
		}
		array[index] = item;
		return array;
	};
}