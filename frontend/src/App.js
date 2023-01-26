import { Routes, Route } from 'react-router-dom';
import Layout from './routes/Layout';
import NoMatch from './routes/NoMatch';
import User from './routes/User';
import TypeAdder from './routes/TypeAdder';

function App() {
	return (
		<Routes>
			<Route path="/" element={<Layout />}>
				<Route path="User" element={<User />} />
				<Route path="*" element={<NoMatch />} />
				<Route path="/type/adder" element={<TypeAdder />} />
			</Route>
		</Routes>
	);
}

export default App;
