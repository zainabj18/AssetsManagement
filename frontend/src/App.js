import { Routes, Route } from 'react-router-dom';
import Layout from './routes/Layout';
import NoMatch from './routes/NoMatch';
import User from './routes/User';

function App() {
	return (
		<Routes>
			<Route path="/" element={<Layout />}>
				<Route path="newuser" element={<User />} />
				<Route path="*" element={<NoMatch />} />
			</Route>
		</Routes>
	);
}

export default App;
