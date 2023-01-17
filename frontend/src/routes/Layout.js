import { Outlet } from 'react-router-dom';

const Layout = () => {
	return (
		<div>
			<h1>Code Groover Asset Manager</h1>
			<Outlet />
		</div>
	);
};

export default Layout;
