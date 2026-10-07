import Logo from "./Logo";

const Header = () => {
  return (
    <header className="bg-transparent absolute top-0 w-screen z-90">
      <div className="container h-20 mx-auto flex items-center">
        <Logo />
        <nav></nav>
      </div>
    </header>
  );
};

export default Header;
