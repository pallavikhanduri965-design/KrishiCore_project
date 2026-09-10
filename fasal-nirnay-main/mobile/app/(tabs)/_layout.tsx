import { Tabs } from 'expo-router';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { COLORS } from '../../src/utils/constants';

type IconName = React.ComponentProps<typeof MaterialCommunityIcons>['name'];

const TABS = [
    { name: 'index', title: 'होम', icon: 'home' },
    { name: 'chat', title: 'सलाहकार', icon: 'robot-outline' },
    { name: 'market', title: 'मंडी', icon: 'chart-bar' },
    { name: 'news', title: 'समाचार', icon: 'newspaper-variant' },
    { name: 'profile', title: 'प्रोफ़ाइल', icon: 'account' },
];

export default function TabLayout() {
    return (
        <Tabs
            screenOptions={{
                headerShown: false,
                tabBarActiveTintColor: COLORS.greenPrimary,
                tabBarInactiveTintColor: '#9E9E9E',
                tabBarStyle: {
                    height: 68,
                    paddingBottom: 10,
                    paddingTop: 6,
                    backgroundColor: 'white',
                    borderTopWidth: 1,
                    borderTopColor: '#E8E8E8',
                    elevation: 16,
                },
                tabBarLabelStyle: { fontSize: 11, fontWeight: '600' },
            }}
        >
            {TABS.map((tab) => (
                <Tabs.Screen
                    key={tab.name}
                    name={tab.name}
                    options={{
                        title: tab.title,
                        tabBarIcon: ({ color, size }) => (
                            <MaterialCommunityIcons name={tab.icon as IconName} size={size + 2} color={color} />
                        ),
                    }}
                />
            ))}
        </Tabs>
    );
}