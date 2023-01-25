import { Routes, Route } from 'react-router-dom';
import AssetViewer from './routes/AssetVeiwer';
import Layout from './routes/Layout';
import NoMatch from './routes/NoMatch';
import KeywordSearch from './routes/KeywordSearch';

function App() {
	return (
		<Routes>
			<Route path="/" element={<Layout />}>
				<Route path="asset/:id" element={<AssetViewer />}/>
				<Route path="*" element={<NoMatch />} />
				<Route path="KeywordSearch" element={<KeywordSearch />} />
			</Route>
		</Routes>
	);
}

export default App;
