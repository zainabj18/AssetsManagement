import { Routes, Route } from 'react-router-dom';
import Layout from './routes/Layout';
import NoMatch from './routes/NoMatch';

function App() {
	return (
		<Routes>
			<Route path="/" element={<Layout />}>
				<Route path="*" element={<NoMatch />} />
			</Route>
		</Routes>
	);
}

export default App;
