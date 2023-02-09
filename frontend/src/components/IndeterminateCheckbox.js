import React from 'react';
/**
 * Adapted from React Table
 * @author React Table https://react-table-v7.tanstack.com/docs/api/useRowSelect
 */
const IndeterminateCheckbox = React.forwardRef(
	({ indeterminate, ...rest }, ref) => {
		const defaultRef = React.useRef();
		const resolvedRef = ref || defaultRef;
  
		React.useEffect(() => {
			resolvedRef.current.indeterminate = indeterminate;
		}, [resolvedRef, indeterminate]);
  
		return (
			<>
				<input type="checkbox" ref={resolvedRef} {...rest} />
			</>
		);
	}
);
export default IndeterminateCheckbox;