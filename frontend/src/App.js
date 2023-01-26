import { Routes, Route } from 'react-router-dom';
import Layout from './routes/Layout';
import NoMatch from './routes/NoMatch';
import FilterBasedSearch from './routes/FilterBasedSearch';

function App() {
	return (
		<Routes>
			<Route path="/" element={<Layout />}>
				<Route path="Filter" element={<FilterBasedSearch />} />
				<Route path="*" element={<NoMatch />} />
			</Route>
		</Routes>
	);
}

export default App;
