import { Routes, Route } from 'react-router-dom';
import AssetViewer from './components/AssetVeiwer';
import CreateAsset from './routes/CreateAsset';
import Layout from './routes/Layout';
import Login from './routes/Login';
import NoMatch from './routes/NoMatch';
import FilterBasedSearch from './routes/FilterBasedSearch';
import User from './routes/User';
import TypeAdder from './routes/TypeAdder';
import { createContext,useMemo,useState } from 'react';

export const AuthContext = createContext({
	setUser: () => null,
	user: null
});

function App() {
	const [user, setUser] = useState({'userID':1,'userType':'ADMIN','userPrivileges':'PUBLIC'});
	const value = useMemo(
		() => ({ user, setUser, }), 
		[user]
	);
	return (
		<AuthContext.Provider value={value}>
			<Routes>
				<Route path="/" element={<Layout />}>
					<Route path="newasset" element={<CreateAsset />} />
					<Route path="asset/:id" element={<AssetViewer canEdit={true} isNew={false}/>} />
					<Route path="login" element={<Login />} />
					<Route path="filter" element={<FilterBasedSearch />} />
					<Route path="user" element={<User />} />
					<Route path="*" element={<NoMatch />} />
					<Route path="type/adder" element={<TypeAdder />} />
				</Route>
			</Routes>
		</AuthContext.Provider>
	);
}

export default App;
