import TypeAdderManager from './TypeAdderManager';

/** Class to hold and use the input data for creating a new attribute */
export default class AttributeMaker {

	/** Gives the message for when there are no input errors when creating an attribute.
	 * @returns An object containg a key for each error message, each representing no error (an empty string).
	*/
	static get_message_noError() {
		return { attributeName: '', num_lmt: '', options: '' };
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
		this.isMulti = false;
	}

	/** Checks for any errors in the user's input.
	 * @param {Array.<{attributeName: string}>} allAttributes The list of attributes that already exist.
	 * @returns An object containg a key between names and their errorMessages.
	 * An empty string for an error message means that there was no error.
	 */
	checkForErrors = (allAttributes) => {
		return {
			attributeName: this.checkForNameError(allAttributes),
			num_lmt: this.checkForMinMaxError(),
			options: this.checkForOptionsError()
		};
	};

	/** Checks for any errors in the name input
	 * @param {Array.<{attributeName: string}>} allAttributes The list of attributes that already exist.
	 * @returns The error message. An empty string represents no error.
	 */
	checkForNameError = (allAttributes) => {
		if (this.name === '') {
			return 'Name is required';
		}
		if (TypeAdderManager.isAttributeNameIn(this.name, allAttributes)) {
			return 'Name already in use';
		}
		return '';
	};

	/** Checks for any errors in the num_lmt input.
	 * @returns The error message. An empty string represents no error.
	 */
	checkForMinMaxError = () => {
		if (this.type === 'num_lmt') {
			if (this.min >= this.max) {
				return 'Minimum must be less than maxmium';
			}
		}
		return '';
	};

	/** Checks for any errors in the options input.
	 * @returns The error message. An empty string represents no error.
	 */
	checkForOptionsError = () => {
		let choices = this.choices.split(',');
		if (this.type === 'options') {
			if (choices.length < 2) {
				return 'There must be at least 2 options';
			}
			if (choices.includes('')) {
				return 'Can not contain an empty option';
			}
		}
		return '';
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
					isMulti: this.isMulti
				}
			};
			return { ...base, ...validation };
		}
		return base;
	};
};