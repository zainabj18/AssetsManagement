import { Routes, Route } from 'react-router-dom';
import AssetViewer from './components/AssetVeiwer';
import Layout from './routes/Layout';
import Login from './routes/Login';
import NoMatch from './routes/NoMatch';
import FilterBasedSearch from './routes/FilterBasedSearch';
import User from './routes/User';
import CreateProject from './routes/CreateProject';
import TypeAdder from './routes/TypeAdder';

function App() {
	return (
		<Routes>
			<Route path="project/new" element={<CreateProject />} />
			<Route path="/" element={<Layout />}>
				<Route
					path="asset/:id"
					element={<AssetViewer canEdit={true} isNew={false} />}
				/>
				<Route path="login" element={<Login />} />
				<Route path="filter" element={<FilterBasedSearch />} />
				<Route path="user" element={<User />} />
				<Route path="*" element={<NoMatch />} />
				<Route path="type/adder" element={<TypeAdder />} />
			</Route>
		</Routes>
	);
}

export default App;
