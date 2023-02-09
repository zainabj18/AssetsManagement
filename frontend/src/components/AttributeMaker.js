import AttributeManager from './AttributeManager';

/** Class to hold and use the input data for creating a new attribute */
export default class AttributeMaker {

	/** Gives the message for when there are no input errors when creating an attribute.
	 * @returns The 'no errors' message (an ampty string).
	*/
	static get_message_noError() {
		return {attributeName: ''};
	}

	/** Creates an empty set of values for a new attribute.
	 * @constructor
	*/
	constructor() {
		this.name = '';
		this.type = '';
		this.min = '';
		this.max = '';
		this.list_type = '';
		this.choices = '';
		this.isMulti=false;
	}

	/** Checks for any errors in the user's input
	 * @param {Array.<{attributeName: string}>} allAttributes The list of attributes that already exist
	 * @returns An object containg a key between names and their errorMessages.
	 * An empty string for an error message means that there was no error.
	 */
	checkForErrors = (allAttributes) => {
		let duplicate = AttributeManager.isAttributeNameIn(this.name, allAttributes);
		let emptyName = this.name === '';

		let name_errorMessage;
		if (emptyName) {
			name_errorMessage = 'Name is required';
		}
		else if (duplicate) {
			name_errorMessage = 'Name already in use';
		}
		else {
			name_errorMessage = '';
		}

		return { attributeName: name_errorMessage };
	};

	/** Forms and returns attribute
	 * @returns The newly formed attribute object
	 */
	formAttribute = () => {
		let base = {
			attributeName: this.name,
			attributeType: this.type
		};
		let validation;

		if (this.type === 'num_lmt') {
			validation = {
				validation: {
					min: this.min,
					max: this.max
				}
			};
			return { ...base, ...validation };
		}

		if (this.type === 'list') {
			validation = {
				validation: {
					type: this.list_type
				}
			};
			return { ...base, ...validation };
		}
		if (this.type === 'options') {
			validation = {
				validation: {
					values: this.choices.split(','),
					isMulti:this.isMulti
				}
			};
			return { ...base, ...validation };
		}
		return base;
	};
};