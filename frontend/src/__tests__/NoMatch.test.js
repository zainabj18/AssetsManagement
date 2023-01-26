
import { render, screen } from '@testing-library/react';
import NoMatch from '../routes/NoMatch';


test('renders the landing page', () => {
	render(<NoMatch />);
	expect(screen.getByText('Sorry Page Not Found!'));
});