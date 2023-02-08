import { Routes, Route } from 'react-router-dom';
import AssetViewer from './components/AssetVeiwer';
import CreateAsset from './routes/assets/CreateAsset';
import Layout from './routes/Layout';
import Login from './routes/Login';
import NoMatch from './routes/NoMatch';
import AssetSearcher from './routes/AssetSearcher';
import User from './routes/User';
import TypeAdder from './routes/TypeAdder';
import KeywordSearch from './routes/KeywordSearch';
import { AuthProvider } from './hooks/useAuth';
import AssetsOverview from './routes/assets/AssetsOverview';
import AssetsLayout from './routes/assets/AssetsLayout';


//TODO:Wrap in error boundary
function App() {

	return (

		<Routes>
			<Route path="KeywordSearch" element={<KeywordSearch />} />
			<Route path="search" element={<AssetSearcher />} />
			<Route path="/login" element={<Login />} />
			<Route path="/" element={<Layout />}>
				<Route path="assets/" element={<AssetsLayout />}>
					<Route index element={<AssetsOverview />} />
					<Route path="new" element={<CreateAsset />} />
					<Route path="view/:id" element={<AssetViewer canEdit={true} isNew={false} />} />
					
				</Route>
				<Route path="user" element={<User />} />
				<Route path="type/adder" element={<TypeAdder />} />
			</Route>
			<Route path="*" element={<NoMatch />} />
		</Routes>

	);
}

export default App;
